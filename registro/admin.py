from django.contrib import admin
from .models import Ocorrencia, Vitima, Agressor, Alerta

# Registre seus modelos no admin
admin.site.register(Ocorrencia)
admin.site.register(Vitima)
admin.site.register(Agressor)
admin.site.register(Alerta)
