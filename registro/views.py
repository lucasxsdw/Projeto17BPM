import pandas as pd
from django.shortcuts import render
from .models import Ocorrencia, Endereco, Assistida, Agressor
from django.contrib import messages

def importar_planilha(request):
    """
    Função responsável por importar dados de uma planilha Excel para o banco de dados.

    Fluxo principal:
    1. Receber e validar o envio do arquivo.
    2. Ler o conteúdo da planilha usando Pandas.
    3. Validar se as colunas obrigatórias estão presentes.
    4. Filtrar apenas os registros de tipos de violência permitidos.
    5. Para cada linha válida:
        - Criar ou associar Endereços de Assistida e Agressor.
        - Criar ou associar Assistida e Agressor.
        - Criar o registro da Ocorrência.
    6. Retornar mensagens de sucesso ou erro.

    Template usado:
    - 'registro/importar.html' para envio e erro
    - 'registro/sucesso.html' para sucesso
    """
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']

        try:
            # 1. Ler a planilha Excel
            df = pd.read_excel(arquivo, engine='openpyxl')
            print("Arquivo carregado com sucesso.")
            print(df.head())  # Debug: Mostrar primeiras linhas

            # 2. Validar colunas obrigatórias
            colunas_esperadas = {
                'nome_assistida', 'rua_assistida', 'numero_assistida', 'bairro_assistida', 'cidade_assistida', 'municipio_assistida',
                'nome_agressor', 'rua_agressor', 'numero_agressor', 'bairro_agressor', 'cidade_agressor', 'municipio_agressor',
                'local_ocorrencia', 'tipo', 'relacao_vitima_autor', 'data'
            }
            if not colunas_esperadas.issubset(df.columns):
                messages.error(request, "A planilha não contém as colunas corretas. Verifique o formato esperado.")
                return render(request, 'registro/importar.html')

            # 3. Filtrar apenas tipos de violência permitidos
            tipos_permitidos = [
                'Violência física', 'Violência psicológica', 'Violência sexual',
                'Ameaça', 'Perseguição', 'Lesão corporal', 'Tentativa de homicídio'
            ]
            total_linhas = len(df)
            df = df[df['tipo'].isin(tipos_permitidos)]  # Filtra o DataFrame
            linhas_filtradas = total_linhas - len(df)

            if linhas_filtradas > 0:
                messages.warning(request, f"{linhas_filtradas} linha(s) ignorada(s) por tipo de violência não permitido.")

            # 4. Converter coluna 'data' para datetime
            df['data'] = pd.to_datetime(df['data'], errors='coerce')

            # 5. Inserir registros no banco de dados
            for index, row in df.iterrows():
                print(f"Importando linha {index+1}: {row.to_dict()}")  # Debug

                if pd.notna(row['data']):
                    # Criar/obter Endereço da Assistida
                    endereco_assistida, _ = Endereco.objects.get_or_create(
                            rua=row['rua_assistida'],
                            numero=row['numero_assistida'],
                            bairro=row['bairro_assistida'],
                            cidade=row['cidade_assistida'],
                            municipio=row['municipio_assistida']
                    )
                    # Verifica campos obrigatórios
                    if not nome_assistida or not nome_agressor or not tipo or pd.isna(data_ocorrencia):
                        print(f"Linha {index+1} ignorada: campos obrigatórios ausentes.")
                        messages.warning(request, f"Linha {index+1} ignorada: campos obrigatórios ausentes.")
                        continue  # Pula esta linha e vai para a próxima
                    
                    
                    
                    # Criar/obter Assistida
                    assistida, _ = Assistida.objects.get_or_create(
                        nome=row['nome_assistida'],
                        endereco=endereco_assistida
                    )

                    # Criar/obter Endereço do Agressor
                    endereco_agressor, _ = Endereco.objects.get_or_create(
                        rua=row['rua_agressor'],
                        numero=row['numero_agressor'],
                        bairro=row['bairro_agressor'],
                        cidade=row['cidade_agressor'],
                        municipio=row['municipio_agressor']
                    )

                    # Criar/obter Agressor
                    agressor, _ = Agressor.objects.get_or_create(
                        nome=row['nome_agressor'],
                        endereco=endereco_agressor
                    )

                    # Criar a Ocorrência
                    Ocorrencia.objects.create(
                        local_ocorrencia=row['local_ocorrencia'],
                        tipo=row['tipo'],
                        relacao_vitima_autor=row.get('relacao_vitima_autor', ''),
                        assistida=assistida,
                        agressor=agressor,
                        data_ocorrencia=row['data']
                    )

            # Se tudo ocorrer bem
            print("Importação concluída com sucesso.")
            messages.success(request, "Dados importados com sucesso!")
            return render(request, 'registro/sucesso.html')

        except Exception as e:
            # Em caso de erro
            print(f"Erro na importação: {str(e)}")
            messages.error(request, f"Erro ao processar a planilha: {str(e)}")
            return render(request, 'registro/importar.html')

    # Se não for POST, apenas exibe a página de importação
    return render(request, 'registro/importar.html')
