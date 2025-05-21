from django.db import models

class OcorrenciaImportada(models.Model):
    
    class Meta:
        db_table = 'ocorrencias'  # Nome da tabela no banco de dados
    
    nome_vitima = models.CharField(max_length=255)
    nome_agressor = models.CharField(max_length=255)
    local_ocorrencia = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    relacao_vitima_autor = models.CharField(max_length=255, null=True, blank=True)
    data_ocorrencia = models.DateField(null=True, blank=True)
    
    rua_vitima = models.CharField(max_length=255)
    numero_vitima = models.CharField(max_length=20)
    bairro_vitima = models.CharField(max_length=100)
    cidade_vitima = models.CharField(max_length=100)
    municipio_vitima = models.CharField(max_length=100)

    rua_agressor = models.CharField(max_length=255)
    numero_agressor = models.CharField(max_length=20)
    bairro_agressor = models.CharField(max_length=100)
    cidade_agressor = models.CharField(max_length=100)
    municipio_agressor = models.CharField(max_length=100)

    data_importacao = models.DateTimeField(auto_now_add=True)
    apagado = models.BooleanField(default=False)  # soft delete
   
    def __str__(self):
        return f"{self.nome_vitima} - {self.tipo} ({self.data_ocorrencia})"
