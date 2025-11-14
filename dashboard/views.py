from django.shortcuts import render
from registro.models import Ocorrencia, Agressor, Vitima, Alerta
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')




def dashboard_view(request):

  
    total_ocorrencias = Ocorrencia.objects.count()

    agressores_reincidentes = Agressor.objects.annotate(
        total_ocorrencias=Count('ocorrencias')
    ).filter(total_ocorrencias__gt=1).count()
    total_agressores = Agressor.objects.count()
    taxa_reincidencia_agressor = round((agressores_reincidentes / total_agressores) * 100, 1) if total_agressores else 0

    vitimas_por_nome = (
        Vitima.objects
        .values('nome')
        .exclude(nome__isnull=True)
        .exclude(nome__exact='')
        .annotate(total_ocorrencias=Count('ocorrencia', distinct=True))
    )
    vitimas_reincidentes = vitimas_por_nome.filter(total_ocorrencias__gt=1).count()
    total_vitimas_distintas = vitimas_por_nome.count()
    taxa_reincidencia_vitimas = round((vitimas_reincidentes / total_vitimas_distintas) * 100, 1) if total_vitimas_distintas else 0.0

    total_domesticas = Ocorrencia.objects.filter(natureza__icontains='violencia domestica').count()
    com_medida = Ocorrencia.objects.filter(
        natureza__icontains='violencia domestica', medida_protetiva=True
    ).count()
    proporcao_medidas = round((com_medida / total_domesticas) * 100, 1) if total_domesticas else 0

    # ==========================
    # 📊 DADOS PARA OS GRÁFICOS
    # ==========================

    # Ocorrências por mês (barras)
    ocorrencias_por_mes = (
        Ocorrencia.objects
        .annotate(mes=TruncMonth('data_registro'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    labels_meses = [o['mes'].strftime('%b/%Y') for o in ocorrencias_por_mes if o['mes']]
    valores_meses = [o['total'] for o in ocorrencias_por_mes]

    # Ocorrências por cidade (pizza)
    ocorrencias_por_cidade = (
        Ocorrencia.objects
        .values('municipio')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]  # top 5 cidades
    )

    labels_cidades = [o['municipio'] or 'Não informado' for o in ocorrencias_por_cidade]
    valores_cidades = [o['total'] for o in ocorrencias_por_cidade]

    context = {
    'total_ocorrencias': total_ocorrencias,
    'taxa_reincidencia_agressor': taxa_reincidencia_agressor,
    'taxa_reincidencia_vitimas': taxa_reincidencia_vitimas,
    'proporcao_medidas': proporcao_medidas,

    # gráficos (agora serializados corretamente)
    'labels_meses': json.dumps(labels_meses),
    'valores_meses': json.dumps(valores_meses),
    'labels_cidades': json.dumps(labels_cidades),
    'valores_cidades': json.dumps(valores_cidades),
}


    return render(request, 'dashboard/index.html', context)







# função auxiliar que gera os alertas
def gerar_alertas_reincidencia():
    reincidentes = (
        Ocorrencia.objects.values('vitimas__nome')
        .annotate(qtd=Count('id'))
        .filter(qtd__gt=1)
        .exclude(vitimas__nome__isnull=True)
        .exclude(vitimas__nome__exact='')
    )

    for r in reincidentes:
        nome = r['vitimas__nome']
        descricao = f"A vítima {nome} possui {r['qtd']} ocorrências registradas."

        if not Alerta.objects.filter(descricao=descricao, ativo=True).exists():
            Alerta.objects.create(
                tipo='VITIMA_REINCIDENTE',
                descricao=descricao
            )


# view que exibe os alertas
def verificar_alertas_reincidencia(request):
    gerar_alertas_reincidencia()  # agora sim, chamando a função auxiliar

    alertas = Alerta.objects.filter(ativo=True).order_by('-data_criacao')[:5]
    context = {'alertas': alertas}
    return render(request, 'dashboard/alert.html', context)