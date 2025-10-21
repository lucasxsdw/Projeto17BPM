from django.urls import path
from . import views

urlpatterns = [

   path('ocorrencias/mes', views.total_ocorrencias_por_mes, name='total_ocorrencias_por_mes'),
   path('ocorrencias/listar/crescimento', views.reincidencia_de_agressores, name='reincidencia_de_agressores'),
   path('ocorrencias/listar/ranking', views.ranking_bairros, name='ranking_bairros'),

]