from django.db import models
from django.contrib.auth.models import User

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
    codigo_procedimento = models.CharField("Código do procedimento", max_length = 8, unique = True)
    nome = models.CharField("Nome", max_length = 250)
    quantidade_procedimento = models.CharField("Quantidade", max_length = 2)
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
    
class CBOs (models.Model):
    codigo_cbo = models.CharField('Código CBO', max_length = 25, unique = True)
    titulo_cbo = models.CharField('Título CBO', max_length = 200, unique = True)

    def __str__(self):
        return self.titulo_cbo
    
class ProfissionalSolicitante(models.Model):
    nome_profissional = models.CharField('Nome do Profissional Solicitante',max_length = 100)
    class Conselho(models.TextChoices):
        CRM = 'CRM', 'CRM'
        CRP = 'CRP', 'CRP'
        CRO = 'CRO', 'CRO'
        COREN = 'CRN', 'COREN'
    class UFConselho(models.TextChoices):
        Acre = 'AC', 'AC'
        Alagoas	= 'AL', 'AL'
        Amapá = 'AP', 'AP'
        Amazonas = 'AM', 'AM'
        Bahia = 'BA', 'BA'
        Ceará = 'CE', 'CE'
        Distrito_Federal = 'DF', 'DF'
        Espírito_Santo = 'ES', 'ES'
        Goiás = 'GO', 'GO'
        Maranhão = 'MA', 'MA'
        Mato_Grosso = 'MT', 'MT'
        Mato_Grosso_do_Sul = 'MS', 'MS'
        Minas_Gerais = 'MG', 'MG'
        Pará = 'PA', 'PA'
        Paraíba = 'PB', 'PB'
        Paraná = 'PR', 'PR'
        Pernambuco = 'PE', 'PE'
        Piauí = 'PI', 'PI'
        Rio_de_Janeiro = 'RJ', 'RJ'
        Rio_Grande_do_Norte = 'RN', 'RN'
        Rio_Grande_do_Sul = 'RS', 'RS'
        Rondônia = 'RO', 'RO'
        Roraima = 'RR', 'RR'
        Santa_Catarina = 'SC', 'SC'
        São_Paulo = 'SP', 'SP'
        Sergipe = 'SE', 'SE'
        Tocantins = 'TO', 'TO'
    
    tipo_conselho = models.CharField('Conselho do Profissional', max_length = 3, choices = Conselho.choices)
    UF_Conselho = models.CharField('UF do Conselho', max_length = 2, choices = UFConselho.choices)
    codigo = models.CharField('Código do Profissional Solicitante', max_length = 20, unique = True)
    cbos = models.ForeignKey(CBOs, on_delete=models.PROTECT)
    

    def __str__(self):
        return self.nome_profissional

class Executante(models.Model):
    CNPJ = models.CharField(max_length = 14, unique = True)
    nome = models.CharField(max_length = 50)
    codigo = models.CharField(max_length = 5, unique = True, blank = True, editable = False)

    def __str__(self):
        return self.nome
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.codigo:
            self.codigo = f'{self.id:05d}'
            super().save(update_fields=['codigo'])

class Solicitacao(models.Model):
    paciente = models.ForeignKey(Beneficiario, on_delete=models.PROTECT)
    profissional_solicitante = models.ForeignKey(ProfissionalSolicitante, on_delete=models.PROTECT)
    executante = models.ForeignKey(Executante, on_delete=models.PROTECT)
    credenciado = models.ForeignKey(User, on_delete=models.PROTECT )

    class CaraterSolicitacao(models.TextChoices):
        URGENTE = 'URG', 'Urgência'
        ELETIVO = 'ELE', 'Eletivo'
    carater_solicitacao = models.CharField('Caráter de Solicitação', max_length = 3, choices = CaraterSolicitacao.choices)
    
    class Status(models.TextChoices):
        APROVADO = 'APV', 'Pedido Aprovado'
        ANALISE = 'ANA', 'Em Análise'
        PENDENTE = 'PEN', 'Pendência'
        NEGADO = 'NEV', 'Negado'
    status = models.CharField('Status do Pedido', max_length = 3, choices = Status.choices)
    data_solicitacao = models.DateField(auto_now_add = True)
    indicacao = models.CharField('Indicação Clínica', max_length=500)
    numero_guia = models.CharField(max_length = 8, unique = True, blank = True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.carater_solicitacao == self.CaraterSolicitacao.URGENTE:
                self.status = self.Status.APROVADO
            else:
                self.status = self.Status.ANALISE
            super().save(*args, **kwargs)
            if not self.numero_guia:
                self.numero_guia = f'{self.id:06d}'
                super().save(update_fields=['numero_guia'])
    
    def __str__(self):
        return f'Solicitação para {self.paciente} (Guia: {self.numero_guia})'
    
class AnexoSolicitacao(models.Model):
    anexo = models.FileField(upload_to='solicitacoes/anexos/%Y/%m/%d/')
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)

class ItemSolicitacao(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, related_name='itens', on_delete=models.CASCADE)
    procedimento = models.ForeignKey(Procedimento, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.procedimento.nome} (Qtd: {self.quantidade})"
    

    
