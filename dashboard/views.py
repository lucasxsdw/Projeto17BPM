from urllib import request
from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Max, Min
from registro.models import Agressor, Ocorrencia




from django.db.models import Count

def total_ocorrencias_por_mes(request):
    # Total de ocorrências
    total_ocorrencias = Ocorrencia.objects.aggregate(total_registro=Count('id'))
    
    # Total de agressores e reincidentes geral
    agressores_reincidentes = Agressor.objects.all()
    total_agressores = agressores_reincidentes.count()
    
    reincidentes = agressores_reincidentes.annotate(
        total=Count('ocorrencias')
    ).filter(total__gt=1).count()
    
    taxa_reincidencia = round((reincidentes / total_agressores) * 100, 2) if total_agressores > 0 else 0

    # =========================
    # Reincidência POR MUNICÍPIO
    # =========================
    municipios = Ocorrencia.objects.values_list('municipio', flat=True).distinct()
    reincidencia_municipio = {}

    for m in municipios:
        agressores_municipio = Agressor.objects.filter(ocorrencias__municipio=m).distinct()
        total_agressores_m = agressores_municipio.count()

        reincidentes_m = agressores_municipio.annotate(
            total=Count('ocorrencias')
        ).filter(total__gt=1).count()

        taxa_m = round((reincidentes_m / total_agressores_m) * 100, 2) if total_agressores_m > 0 else 0
        reincidencia_municipio[m] = taxa_m

    contexto = {
        'totais': total_ocorrencias,
        'taxa_reincidencia': taxa_reincidencia,
        'reincidencia_municipio': reincidencia_municipio
    }
    
    return render(request, 'dashboard/index.html', contexto)








def ranking_bairros():
    return render(request, 'index.html')
