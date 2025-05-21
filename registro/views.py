import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import OcorrenciaImportada

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
    # ======================= INÍCIO DO IMPORTAÇÃO VIA LISTAGEM =======================
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        try:
            df = pd.read_excel(arquivo, engine='openpyxl')

            colunas_esperadas = {
                'nome_vitima','rua_vitima','numero_vitima','bairro_vitima',
                'cidade_vitima','municipio_vitima','nome_agressor','rua_agressor',
                'numero_agressor','bairro_agressor','cidade_agressor','municipio_agressor',
                'local_ocorrencia','tipo','relacao_vitima_autor','data'
            }

            colunas_faltando = colunas_esperadas - set(df.columns)
            if colunas_faltando:
                # Mostra quais colunas estão faltando na planilha
                mensagens_faltando = ", ".join(colunas_faltando)
                messages.error(request, f"A planilha não foi importada porque estão faltando as seguintes colunas obrigatórias: {mensagens_faltando}")
            else:
                tipos_permitidos = [
                    'Violência física','Violência psicológica','Violência sexual',
                    'Ameaça','Perseguição','Lesão corporal','Tentativa de homicídio'
                ]
                total = len(df)
                df = df[df['tipo'].isin(tipos_permitidos)]
                ignoradas = total - len(df)
                if ignoradas:
                    messages.warning(request, f"{ignoradas} linha(s) ignorada(s) por tipo não permitido.")

                df['data'] = pd.to_datetime(df['data'], errors='coerce')
                for i, row in df.iterrows():
                    if pd.isna(row['data']):
                        messages.warning(request, f"Linha {i+1} ignorada: data inválida.")
                        continue
                    OcorrenciaImportada.objects.create(
                        nome_vitima=row['nome_vitima'],
                        rua_vitima=row['rua_vitima'],
                        numero_vitima=row['numero_vitima'],
                        bairro_vitima=row['bairro_vitima'],
                        cidade_vitima=row['cidade_vitima'],  # <- aqui estava o erro
                        municipio_vitima=row['municipio_vitima'],

                        nome_agressor=row['nome_agressor'],
                        rua_agressor=row['rua_agressor'],
                        numero_agressor=row['numero_agressor'],
                        bairro_agressor=row['bairro_agressor'],
                        cidade_agressor=row['cidade_agressor'],
                        municipio_agressor=row['municipio_agressor'],

                        local_ocorrencia=row['local_ocorrencia'],
                        tipo=row['tipo'],
                        relacao_vitima_autor=row.get('relacao_vitima_autor', ''),
                        data_ocorrencia=row['data'],

                 
                    )
                messages.success(request, "Importação concluída com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao processar a planilha: {e}")
    # ======================= FIM DO IMPORTAÇÃO VIA LISTAGEM =======================

    # Fluxo original de exibição
    mostrar_apagados = request.GET.get('apagados') == '1'
    if mostrar_apagados:
        ocorrencias = OcorrenciaImportada.objects.filter(apagado=True).order_by('-data_importacao')
    else:
        ocorrencias = OcorrenciaImportada.objects.filter(apagado=False).order_by('-data_importacao')
    return render(request, 'registro/listar.html', {
        'ocorrencias': ocorrencias,
        'mostrar_apagados': mostrar_apagados
    })


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
