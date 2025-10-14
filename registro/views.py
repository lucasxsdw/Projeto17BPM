import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.db.models import Q
from .models import Ocorrencia, Vitima, Agressor
from .forms import ImportarDadosForm
import re
from datetime import datetime


# =========================
# PÁGINA INICIAL
# =========================
def home(request):
    """Renderiza a página inicial"""
    return render(request, 'index.html')


# =========================
# FORMULÁRIO DE UPLOAD DE PLANILHA
# =========================
class FormOcorrencia(View):
    """
    Classe baseada em View para upload de planilhas Excel contendo ocorrências.
    """

    template_name = 'ocorrencias/ocorrencia_form.html'

    def get(self, request):
        """Exibe o formulário de upload"""
        form = ImportarDadosForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Processa o arquivo enviado via formulário"""
        form = ImportarDadosForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        arquivo = request.FILES['arquivo']

        try:
            df = pd.read_excel(arquivo)
        except Exception as e:
            messages.error(request, f"Erro ao ler o arquivo Excel: {str(e)}")
            return render(request, self.template_name, {'form': form})

        # Normaliza nomes das colunas
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # Itera sobre as linhas da planilha
        for _, row in df.iterrows():
            self.criar_ocorrencia(row)

        messages.success(request, "Planilha processada com sucesso!")
        return redirect('listar_ocorrencias')

    # =========================
    # FUNÇÕES AUXILIARES
    # =========================
    def separar_envolvidos(self, envolvidos_raw):
        """
        Divide o campo de envolvidos em listas de vítimas e agressores.
        Exemplo de entrada:
        "Maria (vítima); João (autor); Pedro (testemunha)"
        """
        vitimas, agressores = [], []

        if not isinstance(envolvidos_raw, str):
            return vitimas, agressores

        partes = re.split(r'[,\n;]+', envolvidos_raw)

        for parte in partes:
            parte = parte.strip()
            match = re.match(r'(.+?)\s*\((.*?)\)', parte)
            if not match:
                continue

            nome = match.group(1).strip()
            papel = match.group(2).strip().lower()

            if 'vítima' in papel or 'vitima' in papel:
                vitimas.append(nome)
            elif 'autor' in papel or 'agressor' in papel:
                agressores.append(nome)

        return vitimas, agressores

    def criar_ocorrencia(self, row):
        """
        Cria ou atualiza uma ocorrência, vinculando vítimas e agressores.
        """

        # Filtra apenas ocorrências de violência doméstica
        natureza = str(row.get('natureza_da_ocorrencia', '')).lower()
        if 'violencia domestica' not in natureza:
            return

        # Converte a data de registro
        data_raw = row.get('data_registro')
        data_registro = timezone.now().date()

        if pd.notna(data_raw):
            try:
                if isinstance(data_raw, str):
                    data_registro = datetime.strptime(data_raw.split(' ')[0], '%d/%m/%Y').date()
                else:
                    data_registro = data_raw.date()
            except Exception:
                pass

        # Cria ou atualiza ocorrência
        ocorrencia, created = Ocorrencia.objects.get_or_create(
            numero_procedimento=row.get('nº_do_procedimento') or row.get('numero_do_procedimento'),
            defaults={
                'data_registro': data_registro,
                'municipio': row.get('municipio'),
                'natureza': row.get('natureza_da_ocorrencia'),
                'unidade_registro': row.get('unidade_de_registro'),
                'unidade_apuracao': row.get('unidade_de_apuracao'),
                'envolvidos_raw': row.get('envolvidos'),
                'processed': False,
            }
        )

        # Extrai vítimas e agressores
        vitimas, agressores = self.separar_envolvidos(row.get('envolvidos'))

        # Cadastra vítimas e agressores sem duplicar
        for nome in vitimas:
            if nome:
                Vitima.objects.get_or_create(ocorrencia=ocorrencia, nome=nome)

        for nome in agressores:
            if nome:
                Agressor.objects.get_or_create(ocorrencia=ocorrencia, nome=nome)


# ==========================
# LISTAGEM DE OCORRÊNCIAS
# ==========================
def listar_ocorrencias(request):
    """
    Exibe todas as ocorrências cadastradas com filtros opcionais:
    - nome da vítima
    - nome do agressor
    - tipo de violência (natureza)
    - município (ou unidade de registro)
    - data inicial e final
    """

    ocorrencias = Ocorrencia.objects.all()

    # Filtros via GET
    nome_vitima = request.GET.get('vitima')
    nome_agressor = request.GET.get('agressor')
    tipo_violencia = request.GET.get('violencia')
    municipio = request.GET.get('municipio')
    data_inicio = request.GET.get('inicio')
    data_fim = request.GET.get('fim')

    # --- FILTROS DINÂMICOS ---
    if nome_vitima:
        ocorrencias = ocorrencias.filter(vitimas__nome__icontains=nome_vitima)

    if nome_agressor:
        ocorrencias = ocorrencias.filter(agressores__nome__icontains=nome_agressor)

    if tipo_violencia:
        ocorrencias = ocorrencias.filter(natureza__icontains=tipo_violencia)

    if municipio:
        ocorrencias = ocorrencias.filter(municipio__icontains=municipio)

    if data_inicio:
        ocorrencias = ocorrencias.filter(data_registro__gte=data_inicio)

    if data_fim:
        ocorrencias = ocorrencias.filter(data_registro__lte=data_fim)

    ocorrencias = ocorrencias.distinct()

    context = {
        'ocorrencias': ocorrencias,
        'filtros': {
            'vitima': nome_vitima,
            'agressor': nome_agressor,
            'violencia': tipo_violencia,
            'municipio': municipio,
            'inicio': data_inicio,
            'fim': data_fim,
        }
    }

    return render(request, 'ocorrencias/ocorrencias_list.html', context)
