from django.shortcuts import render
from registro.models import Ocorrencia, Agressor, Vitima
from django.db.models import Count

def dashboard_view(request):
    """
    Exibe estatísticas gerais: total de ocorrências, taxa de reincidência
    e proporção de medidas protetivas.
    """

    # ================================
    # 1️⃣ TOTAL DE OCORRÊNCIAS
    # ================================
    total_ocorrencias = Ocorrencia.objects.count()

    # ================================
    # 2️⃣ TAXA DE REINCIDÊNCIA DE AGRESSORES
    # ================================
    # Conta quantos agressores aparecem em mais de uma ocorrência
    agressores_reincidentes = Agressor.objects.annotate(
        total_ocorrencias=Count('ocorrencias')
    ).filter(total_ocorrencias__gt=1).count()

    total_agressores = Agressor.objects.count()

    taxa_reincidencia_agressor = 0
    if total_agressores > 0:
        taxa_reincidencia_agressor = round((agressores_reincidentes / total_agressores) * 100, 1)

       
    # 3) Taxa de reincidência de vítimas
    # Contamos vítimas distintas por nome e verificamos quantas têm >1 ocorrência
    vitimas_por_nome = (
        Vitima.objects
        .values('nome')
        .exclude(nome__isnull=True)
        .exclude(nome__exact='')
        .annotate(total_ocorrencias=Count('ocorrencia', distinct=True))
    )

    vitimas_reincidentes = vitimas_por_nome.filter(total_ocorrencias__gt=1).count()
    total_vitimas_distintas = vitimas_por_nome.count()

    taxa_reincidencia_vitimas = round((vitimas_reincidentes / total_vitimas_distintas) * 100, 1) if total_vitimas_distintas > 0 else 0.0

    
   
   
    # ================================
    # 3️⃣ TAXA DE MEDIDAS PROTETIVAS
    # ================================
    total_domesticas = Ocorrencia.objects.filter(
        natureza__icontains='violencia domestica'
    ).count()

    com_medida = Ocorrencia.objects.filter(
        natureza__icontains='violencia domestica',
        medida_protetiva=True
    ).count()

    proporcao_medidas = 0
    if total_domesticas > 0:
        proporcao_medidas = round((com_medida / total_domesticas) * 100, 1)

    # ================================
    # CONTEXTO FINAL
    # ================================
    context = {
        'total_ocorrencias': total_ocorrencias,
        'taxa_reincidencia_agressor': taxa_reincidencia_agressor,
        'taxa_reincidencia_vitimas': taxa_reincidencia_vitimas,
        'proporcao_medidas': proporcao_medidas,
       
    }

    return render(request, 'dashboard/index.html', context)
