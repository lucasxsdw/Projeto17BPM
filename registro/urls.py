from django.urls import path
from . import views

urlpatterns = [
    #Esse arquivo define as rotas do app registro. A rota /importar/ vai abrir o formulário de upload da planilha.
    path('importar/', views.importar_planilha, name='importar'),
]

