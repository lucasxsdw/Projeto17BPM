import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import OcorrenciaImportada







def home(request):
    return render(request, 'index.html')



def form_ocorrencia(request):
    return render(request, 'ocorrencias/ocorrencia_form.html')



def importar_planilha(request):
    # sua view de import separada permanece inalterada,
    # mas não será mais usada pelo template de listagem (já sem rota)
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        try:
            df = pd.read_excel(arquivo, engine='openpyxl')
            # ... resto do seu código original de importação ...
            messages.success(request, "Importação concluída com sucesso!")
            return render(request, 'registro/listar.html', {
                'ocorrencias': OcorrenciaImportada.objects.filter(apagado=False).order_by('-data_importacao')
            })
        except Exception as e:
            messages.error(request, f"Erro ao processar a planilha: {e}")
            return render(request, 'registro/listar.html')
    return render(request, 'registro/listar.html')


def listar_ocorrencias(request):
    ocorrencias = OcorrenciaImportada.objects.all()
    return render(request, 'ocorrencias/ocorrencias_list.html')


def deletar_ocorrencia(request, id):
    ocorrencia = get_object_or_404(OcorrenciaImportada, id=id)
    ocorrencia.apagado = True
    ocorrencia.save()
    messages.success(request, "Ocorrência marcada como apagada.")
    return redirect('listar_ocorrencias')


def restaurar_ocorrencia(request, id):
    ocorrencia = get_object_or_404(OcorrenciaImportada, id=id)
    ocorrencia.apagado = False
    ocorrencia.save()
    messages.success(request, "Ocorrência restaurada com sucesso.")
    return redirect('listar_ocorrencias')
