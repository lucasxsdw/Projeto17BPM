from django.db import models

class OcorrenciaImportada(models.Model):
    
    class Meta:
        db_table = 'ocorrencias'  # Nome da tabela no banco de dados
    
    nome_assistida = models.CharField(max_length=255)
    nome_agressor = models.CharField(max_length=255)
    local_ocorrencia = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    relacao_vitima_autor = models.CharField(max_length=255, null=True, blank=True)
    data_ocorrencia = models.DateField(null=True, blank=True)
    
    rua_assistida = models.CharField(max_length=255)
    numero_assistida = models.CharField(max_length=10)
    bairro_assistida = models.CharField(max_length=100)
    cidade_assistida = models.CharField(max_length=100)
    municipio_assistida = models.CharField(max_length=100)

    
    rua_agressor = models.CharField(max_length=255)
    numero_agressor = models.CharField(max_length=10)
    bairro_agressor = models.CharField(max_length=100)
    cidade_agressor = models.CharField(max_length=100)
    municipio_agressor = models.CharField(max_length=100)

    data_importacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_assistida} - {self.tipo} ({self.data_ocorrencia})"
