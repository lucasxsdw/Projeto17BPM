from django.urls import path
from . import views

urlpatterns = [

   path('ocorrencias/mes', views.total_ocorrencias_por_mes, name='total_ocorrencias_por_mes'),
   #path('dashboard/', views.dashboard, name='dashboard'),

]