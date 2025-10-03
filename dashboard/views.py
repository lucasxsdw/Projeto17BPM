from urllib import request
from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Max, Min

from registro.models import Ocorrencia






def total_ocorrencias_por_mes(request):
    total_ocorrencias = Ocorrencia.objects.aggregate(
        total_registro = Count('id')
        
    )
    

    contexto = {
        'totais': total_ocorrencias, 
    }

    return render(request, 'dashboard/index.html', contexto)

    
    




def percentual_crescimento_mensal():
    return render(request, 'indexs.html')



def ranking_bairros():
    return render(request, 'indexf.html')
