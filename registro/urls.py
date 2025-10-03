from django.urls import path
from . import views
from .views import form_ocorrencia
urlpatterns = [

    path('', views.home, name='home'), 

   path('ocorrencias/importar/', form_ocorrencia.as_view(), name='ocorrencia_form'),
   path('ocorrencias/listar', views.listar_ocorrencias, name='listar_ocorrencias'),
   # path('ocorrencias/deletar/<int:id>/', views.deletar_ocorrencia, name='deletar_ocorrencia'),
   # path('ocorrencias/restaurar/<int:id>/', views.restaurar_ocorrencia, name='restaurar_ocorrencia'),
 
   

]

