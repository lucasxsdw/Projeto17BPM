import pandas as pd
from django.shortcuts import render
from django.contrib import messages
from .models import OcorrenciaImportada

def importar_planilha(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']

        try:
            df = pd.read_excel(arquivo, engine='openpyxl')
            print("Arquivo carregado com sucesso.")
            print(df.head())

            colunas_esperadas = {
                'nome_assistida', 'rua_assistida', 'numero_assistida', 'bairro_assistida', 'cidade_assistida', 'municipio_assistida',
                'nome_agressor', 'rua_agressor', 'numero_agressor', 'bairro_agressor', 'cidade_agressor', 'municipio_agressor',
                'local_ocorrencia', 'tipo', 'relacao_vitima_autor', 'data'
            }
            if not colunas_esperadas.issubset(df.columns):
                messages.error(request, "A planilha não contém as colunas corretas.")
                return render(request, 'registro/importar.html')

            tipos_permitidos = [
                'Violência física', 'Violência psicológica', 'Violência sexual',
                'Ameaça', 'Perseguição', 'Lesão corporal', 'Tentativa de homicídio'
            ]
            total_linhas = len(df)
            df = df[df['tipo'].isin(tipos_permitidos)]
            linhas_filtradas = total_linhas - len(df)

            if linhas_filtradas > 0:
                messages.warning(request, f"{linhas_filtradas} linha(s) ignorada(s) por tipo não permitido.")

            df['data'] = pd.to_datetime(df['data'], errors='coerce')

            for index, row in df.iterrows():
                print(f"Importando linha {index+1}: {row.to_dict()}")

                if pd.isna(row['data']):
                    messages.warning(request, f"Linha {index+1} ignorada: data inválida.")
                    continue

                OcorrenciaImportada.objects.create(
                    nome_assistida=row['nome_assistida'],
                    nome_agressor=row['nome_agressor'],
                    local_ocorrencia=row['local_ocorrencia'],
                    tipo=row['tipo'],
                    relacao_vitima_autor=row.get('relacao_vitima_autor', ''),
                    data_ocorrencia=row['data'],

                    rua_assistida=row['rua_assistida'],
                    numero_assistida=row['numero_assistida'],
                    bairro_assistida=row['bairro_assistida'],
                    cidade_assistida=row['cidade_assistida'],
                    municipio_assistida=row['municipio_assistida'],

                    rua_agressor=row['rua_agressor'],
                    numero_agressor=row['numero_agressor'],
                    bairro_agressor=row['bairro_agressor'],
                    cidade_agressor=row['cidade_agressor'],
                    municipio_agressor=row['municipio_agressor']
                )

            messages.success(request, "Importação concluída com sucesso!")
            return render(request, 'registro/sucesso.html')

        except Exception as e:
            print(f"Erro ao importar: {str(e)}")
            messages.error(request, f"Erro ao processar a planilha: {str(e)}")
            return render(request, 'registro/importar.html')

    return render(request, 'registro/importar.html')
