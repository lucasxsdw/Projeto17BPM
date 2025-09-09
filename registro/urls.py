from django.urls import path
from . import views
from .views import form_ocorrencia, listar_ocorrencias
urlpatterns = [

    path('', views.home, name='home'), 

   path('ocorrencias/importar/', form_ocorrencia.as_view(), name='ocorrencia_form'),
   path('ocorrencias/listar', listar_ocorrencias.as_view(), name='listar_ocorrencias'),
   # path('ocorrencias/deletar/<int:id>/', views.deletar_ocorrencia, name='deletar_ocorrencia'),
   # path('ocorrencias/restaurar/<int:id>/', views.restaurar_ocorrencia, name='restaurar_ocorrencia'),
 
   

]

