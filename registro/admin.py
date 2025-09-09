from django.contrib import admin
from .models import Assistida, Agressor,Ocorrencia,PerfilAcesso, Usuario, Alerta

# Registre seus modelos no admin
admin.site.register(Assistida)
admin.site.register(Agressor)
admin.site.register(Ocorrencia)
admin.site.register(PerfilAcesso)
admin.site.register(Usuario)
admin.site.register(Alerta)

