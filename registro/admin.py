from django.contrib import admin
from .models import Ocorrencia, Assistida, Agressor, Endereco

# Registre seus modelos no admin
admin.site.register(Ocorrencia)
admin.site.register(Assistida)
admin.site.register(Agressor)
admin.site.register(Endereco)
