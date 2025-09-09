import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Assistida, Agressor,Ocorrencia,PerfilAcesso, Usuario, Alerta
from django.views import View
from django.views.generic import ListView

from .forms import ImportarDadosForm




def home(request):
    return render(request, 'index.html')



class form_ocorrencia(View):
    template_name = 'ocorrencias/ocorrencia_form.html'

    def get(self, request):
        """
        Método GET: renderiza o formulário de upload da planilha.
        """
        form = ImportarDadosForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Método POST: processa o arquivo enviado pelo formulário.
        """
        form = ImportarDadosForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = request.FILES['arquivo']
            df = pd.read_excel(arquivo)  # Lê o Excel como DataFrame

            for _, row in df.iterrows():
                # Para cada linha da planilha, cria ou atualiza as entidades
                self.criar_ocorrencia(row)

            return redirect('listar_ocorrencias')  # Redireciona após o processamento

        # Se o formulário não for válido, renderiza o template com erros
        return render(request, self.template_name, {'form': form})

    def criar_ocorrencia(self, row):
        """
        Cria ou atualiza Assistida, Agressor e Ocorrencia usando os dados da linha.
        """

        # 1️⃣ Criar ou obter Assistida
        assistida, _ = Assistida.objects.get_or_create(
            nome_completo=row['nome_assistida'],
            defaults={
                'data_nascimento': row.get('data_nascimento_assistida'),
                'estado_civil': row.get('estado_civil'),
                'escolaridade': row.get('escolaridade'),
                'profissao': row.get('profissao'),
                'rua': row.get('rua'),
                'numero': row.get('numero'),
                'bairro': row.get('bairro'),
                'cidade': row.get('cidade'),
                'municipio': row.get('municipio'),
            }
        )

        # 2️⃣ Criar ou obter Agressor
        agressor, _ = Agressor.objects.get_or_create(
            nome_completo=row['nome_agressor'],
            defaults={
                'data_nascimento': row.get('data_nascimento_agressor'),
                'relacao_com_assistida': row.get('relacao_com_assistida'),
                'rua': row.get('rua_agressor'),
                'numero': row.get('numero_agressor'),
                'bairro': row.get('bairro_agressor'),
                'cidade': row.get('cidade_agressor'),
                'municipio': row.get('municipio_agressor'),
            }
        )

        # 3️⃣ Criar Ocorrencia
        Ocorrencia.objects.create(
            assistida=assistida,
            agressor=agressor,
            local_ocorrencia=row.get('local_ocorrencia'),
            data_ocorrencia=row.get('data_ocorrencia'),
            tipo_violencia=row.get('tipo_violencia'),
            descricao_fato=row.get('descricao_fato'),
            
        )







class listar_ocorrencias(ListView):
    model = Ocorrencia
    template_name = 'ocorrencias/ocorrencias_list.html'
    context_object_name = 'ocorrencias'
