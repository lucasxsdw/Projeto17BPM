from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'), 

    #Esse arquivo define as rotas do app registro. A rota /importar/ vai abrir o formulário de upload da planilha.
    #path('importar/', views.importar_planilha, name='importar'),
    path('ocorrencias/', views.listar_ocorrencias, name='listar_ocorrencias'),
    path('ocorrencias/deletar/<int:id>/', views.deletar_ocorrencia, name='deletar_ocorrencia'),
    path('ocorrencias/restaurar/<int:id>/', views.restaurar_ocorrencia, name='restaurar_ocorrencia'),
    path('ocorrencias/importar/', views.form_ocorrencia, name='ocorrencia_form'),
   

]

