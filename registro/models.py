# apps/ocorrencias/models.py
from django.db import models

SEX_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
)

# ==========================
#  OCORRÊNCIAS PRINCIPAIS
# ==========================
class Ocorrencia(models.Model):
    agressores = models.ManyToManyField('Agressor', related_name='ocorrencias')
    numero_procedimento = models.CharField("Número do procedimento", max_length=120, db_index=True)
    data_registro = models.DateField("Data do registro", null=True, blank=True, db_index=True)
    municipio = models.CharField("Município", max_length=150, null=True, blank=True, db_index=True)
    natureza = models.CharField("Natureza da ocorrência", max_length=255, null=True, blank=True)
    unidade_registro = models.CharField("Unidade de registro", max_length=255, null=True, blank=True)
    unidade_apuracao = models.CharField("Unidade de apuração", max_length=255, null=True, blank=True)
    medida_protetiva = models.BooleanField("Possui medida protetiva?", default=False)

    # Coluna bruta da planilha (texto completo da célula "envolvidos")
    envolvidos_raw = models.TextField("Envolvidos (raw)", null=True, blank=True)

    # Opcional: armazenar dados processados no formato JSON
    parsed_envolvidos = models.JSONField("Envolvidos (parsed)", null=True, blank=True)

    processed = models.BooleanField("Processado", default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"
        ordering = ['municipio', 'data_registro']

    def __str__(self):
        return f"{self.numero_procedimento} — {self.municipio} — {self.data_registro}"

    def vitimas_count(self):
        return self.vitimas.count()

    def agressores_count(self):
        return self.agressores.count()


# ==========================
#  VÍTIMAS E AGRESSORES
# ==========================
class Vitima(models.Model):
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name='vitimas')
    nome = models.CharField("Nome", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vítima"
        verbose_name_plural = "Vítimas"

    def __str__(self):
        return self.nome or f"Vítima #{self.pk}"


class Agressor(models.Model):
    nome = models.CharField("Nome", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agressor"
        verbose_name_plural = "Agressores"

    def __str__(self):
        return self.nome or f"Agressor #{self.pk}"


# ==========================
#  ALERTAS AUTOMÁTICOS
# ==========================
class Alerta(models.Model):
    """
    Armazena os alertas gerados automaticamente pelo sistema.
    """
    titulo_alerta = models.CharField("Título do alerta", max_length=255)
    descricao = models.TextField("Descrição")
    data_hora_alerta = models.DateTimeField("Data/Hora do alerta", auto_now_add=True)
    localidade_alvo = models.CharField("Localidade alvo", max_length=100, null=True, blank=True)
    status_email_enviado = models.BooleanField("E-mail enviado", default=False)

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        db_table = 'alertas'
        ordering = ['-data_hora_alerta']

    def __str__(self):
        return self.titulo_alerta
