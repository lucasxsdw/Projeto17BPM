import pandas as pd
import re
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.db.models import Q
from .models import Ocorrencia, Vitima, Agressor
from .forms import ImportarDadosForm
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
        Extrai vítimas e agressores do campo 'envolvidos', mesmo quando há múltiplos papéis.
        Exemplo:
        "JOÃO (AUTOR), MARIA (COMUNICANTE, VÍTIMA)" -> separa corretamente.
        """
        vitimas, agressores = [], []

        if not isinstance(envolvidos_raw, str):
            return vitimas, agressores

        # Captura pares de Nome + (Papéis)
        matches = re.findall(r'([^,;]+?)\s*\(([^)]+)\)', envolvidos_raw, re.IGNORECASE)

        for nome, papeis in matches:
            nome = nome.strip().title()
            papeis = papeis.lower()

            # Normaliza acentuação
            papeis = (
                papeis.replace("í", "i")
                      .replace("á", "a")
                      .replace("ã", "a")
                      .replace("é", "e")
                      .replace("ê", "e")
                      .replace("ó", "o")
            )

            # Divide os papéis internos (ex: "comunicante, vitima")
            papeis_lista = [p.strip() for p in re.split(r'[,\s;/]+', papeis) if p.strip()]

            # Marca se contém vitima ou autor
            tem_vitima = any('vitima' in p for p in papeis_lista)
            tem_autor = any('autor' in p for p in papeis_lista)

            # Só adiciona se realmente for vítima ou autor
            if tem_vitima:
                vitimas.append(nome)
            if tem_autor:
                agressores.append(nome)

        return vitimas, agressores

    def criar_ocorrencia(self, row):
        """
        Cria ou atualiza uma ocorrência, vinculando vítimas e agressores.
        """

         # Texto completo da natureza
        natureza_texto = str(row.get('natureza_da_ocorrencia', '')).lower()

        
        if 'violencia domestica' not in natureza_texto:
            return
        
        # =========================
        # VERIFICA SE HÁ MEDIDA PROTETIVA
        # =========================
        termos_medida = [
            'medida protetiva',
            'descumprimento de medida protetiva',
            'violação de medida protetiva'
        ]
        tem_medida_protetiva = any(termo in natureza_texto for termo in termos_medida)


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
        ocorrencia, _ = Ocorrencia.objects.get_or_create(
            numero_procedimento=row.get('nº_do_procedimento') or row.get('numero_do_procedimento'),
            defaults={
                'data_registro': data_registro,
                'municipio': row.get('municipio'),
                'natureza': row.get('natureza_da_ocorrencia'),
                'unidade_registro': row.get('unidade_de_registro'),
                'unidade_apuracao': row.get('unidade_de_apuracao'),
                'envolvidos_raw': row.get('envolvidos'),
                'processed': False,
                'medida_protetiva': tem_medida_protetiva,
            }
        )

        # Extrai vítimas e agressores
        vitimas, agressores = self.separar_envolvidos(row.get('envolvidos'))

        # Se não encontrou nenhum, apenas registra log
        if not vitimas and not agressores:
            print(f"[AVISO] Nenhum envolvido encontrado: {row.get('numero_do_procedimento')}")
            return

        # Cadastra vítimas e agressores sem duplicar
        for nome in vitimas:
            if nome:
                Vitima.objects.get_or_create(ocorrencia=ocorrencia, nome=nome)


        for nome in agressores:
            if nome:
                agressor_obj, _ = Agressor.objects.get_or_create(nome=nome)
                ocorrencia.agressores.add(agressor_obj)


# ==========================
# LISTAGEM DE OCORRÊNCIAS
# ==========================


def listar_ocorrencias(request): 
    """
    Exibe todas as ocorrências cadastradas com filtros opcionais.
    """

    ocorrencias = Ocorrencia.objects.all()

    # Filtros via GET
    nome_vitima = request.GET.get('vitima')
    nome_agressor = request.GET.get('agressor')
    tipo_violencia = request.GET.get('violencia')
    municipio = request.GET.get('municipio')
    data_registro = request.GET.get('registro')
    
    # ==========================
    # FILTROS
    # ==========================

    if nome_vitima:
        ocorrencias = ocorrencias.filter(vitimas__nome__icontains=nome_vitima)

    if nome_agressor:
        ocorrencias = ocorrencias.filter(agressores__nome__icontains=nome_agressor)

    if tipo_violencia:
        ocorrencias = ocorrencias.filter(natureza__icontains=tipo_violencia)

    if municipio:
        ocorrencias = ocorrencias.filter(municipio__icontains=municipio)

    # Filtro de data 
    if data_registro:
        try:
            data_formatada = datetime.strptime(data_registro, "%Y-%m-%d").date()
            ocorrencias = ocorrencias.filter(data_registro=data_formatada)
        except ValueError:
            pass  # ignora se a data for inválida

    # Remove duplicados
    ocorrencias = ocorrencias.distinct()

    # Contexto
    context = {
        'ocorrencias': ocorrencias,
        'filtros': {
            'vitima': nome_vitima,
            'agressor': nome_agressor,
            'violencia': tipo_violencia,
            'municipio': municipio,
            'registro': data_registro,
        }
    }

    return render(request, 'ocorrencias/ocorrencias_list.html', context)
