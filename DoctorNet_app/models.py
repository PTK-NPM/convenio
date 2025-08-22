from django.db import models

class Beneficiario(models.Model):
    nome = models.CharField(max_length = 150)
    CPF = models.CharField(max_length = 11, unique = True)
    data_nascimento = models.DateField()
    carteirinha = models.CharField(max_length = 10, unique = True, blank = True, editable = False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.carteirinha:
            self.carteirinha = f'{self.id:08d}'
            super().save(update_fields=['carteirinha'])

class Procedimento(models.Model):
    codigo = models.CharField("Código do procedimento", max_length = 8, unique = True)
    nome = models.CharField("Nome", max_length = 250)
    class Categoria(models.TextChoices):
        IMAGEM = 'IMG', 'Exame de Imagem'
        LABORATORIAL = 'LAB', 'Exame Laboratorial'
        CONSULTA = 'CON', 'Consulta Médica'
        TERAPIA = 'TER', 'Terapia'
        PEQUENA_CIRURGIA = 'PQN', 'Pequena Cirurgia'
        OUTRO = 'OUT', 'Outro'
    categoria = models.CharField("Categoria", max_length = 3, choices = Categoria.choices)

    def __str__(self):
        return self.nome

class ProfissionalSolicitante(models.Model):
    nome_profissional = models.CharField(max_length = 100)
    class Conselho(models.TextChoices):
        CRM = 'CRM', 'CRM'
        CRP = 'CRP', 'CRP'
        CRO = 'CRO', 'CRO'
        COREN = 'CRN', 'COREN'
    conselho = models.CharField('Conselho do Profissional', max_length = 3, choices = Conselho.choices)
    codigo = models.CharField('Código do Profissional Solicitante', max_length = 20)

    def __str__(self):
        return self.nome_profissional

class Executante(models.Model):
    CNPJ = models.CharField(max_length = 14, unique = True)
    nome = models.CharField(max_length = 50)

    def __str__(self):
        return self.nome

