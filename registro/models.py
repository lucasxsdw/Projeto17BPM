from django.db import models

# Tabela Endereço
class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro} ({self.cidade}/{self.municipio})"

# Tabela Assistida
class Assistida(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Assistida"
        verbose_name_plural = "Assistidas"

    def __str__(self):
        return self.nome

# Tabela Agressor
class Agressor(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Agressor"
        verbose_name_plural = "Agressores"

    def __str__(self):
        return self.nome

# Tabela Ocorrência
class Ocorrencia(models.Model):
    local_ocorrencia = models.CharField(max_length=300, default='Local não informado')
    tipo = models.CharField(max_length=300, default='Tipo não informado')
    relacao_vitima_autor = models.CharField(max_length=300, blank=True, null=True)
    data_ocorrencia = models.DateField(blank=True, null=True)
    assistida = models.ForeignKey(Assistida, on_delete=models.PROTECT)
    agressor = models.ForeignKey(Agressor, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'ocorrencias'
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"

    def __str__(self):
        data = self.data_ocorrencia.strftime('%d/%m/%Y') if self.data_ocorrencia else "Data não informada"
        return f"{self.tipo} em {data} - {self.local_ocorrencia}"
