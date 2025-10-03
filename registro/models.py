# seu_projeto/sua_app/models.py
from datetime import date
from django.db import models

class Assistida(models.Model):
    """
    Representa a vítima da ocorrência de violência.
    """
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    estado_civil = models.CharField(max_length=50, null=True, blank=True)
    escolaridade = models.CharField(max_length=100, null=True, blank=True)
    profissao = models.CharField(max_length=100, null=True, blank=True)
    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome_completo
        
    class Meta:
        db_table = 'assistidas'


class Agressor(models.Model):
    """
    Representa a pessoa que cometeu a violência.
    """
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    relacao_com_assistida = models.CharField(max_length=100, null=True, blank=True)
    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome_completo

    class Meta:
        db_table = 'agressores'



class Ocorrencia(models.Model):
    """
    Representa o registro da ocorrência, com chaves estrangeiras para Assistida e Agressor.
    """
    assistida = models.ForeignKey(Assistida, on_delete=models.CASCADE, related_name='ocorrencias')
    agressor = models.ForeignKey(Agressor, on_delete=models.CASCADE, related_name='ocorrencias')
    
    local_ocorrencia = models.CharField(max_length=255)
    data_ocorrencia = models.DateField()
    tipo_violencia = models.CharField(max_length=255)
    descricao_fato = models.TextField(null=True, blank=True)
    
    
    
    # Campos de controle
    data_importacao = models.DateTimeField(auto_now_add=True)
    apagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Ocorrência de {self.tipo_violencia} em {self.local_ocorrencia} - {self.data_ocorrencia}"

    class Meta:
        db_table = 'ocorrencias'


# NOVAS ENTIDADES PARA O ESTÁGIO 2

class PerfilAcesso(models.Model):
    """
    Define os perfis de usuário, como 'Administrador' e 'Analista'.
    """
    nome_perfil = models.CharField(max_length=50, unique=True)
    permissoes_json = models.JSONField(default=dict)

    def __str__(self):
        return self.nome_perfil

    class Meta:
        db_table = 'perfis_acesso'


class Usuario(models.Model):
    """
    Representa um usuário do sistema com controle de acesso.
    """
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=255) # Armazene o hash da senha, não a senha em texto
    ativo = models.BooleanField(default=True)
    perfil = models.ForeignKey(PerfilAcesso, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'usuarios'


class Alerta(models.Model):
    """
    Armazena os alertas gerados automaticamente pelo sistema.
    """
    titulo_alerta = models.CharField(max_length=255)
    descricao = models.TextField()
    data_hora_alerta = models.DateTimeField(auto_now_add=True)
    localidade_alvo = models.CharField(max_length=100)
    status_email_enviado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo_alerta

    class Meta:
        db_table = 'alertas'