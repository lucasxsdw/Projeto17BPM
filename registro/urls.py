from django.urls import path
from . import views
from .views import FormOcorrencia  # note o F maiúsculo, mudou do antigo form_ocorrencia

urlpatterns = [
    path('', views.home, name='home'),
    path('ocorrencias/importar/', FormOcorrencia.as_view(), name='ocorrencia_form'),
    path('ocorrencias/listar/', views.listar_ocorrencias, name='listar_ocorrencias'),
]
