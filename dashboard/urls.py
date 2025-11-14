from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('alertas/', views.verificar_alertas_reincidencia, name='verificar_alertas_reincidencia'),
]
