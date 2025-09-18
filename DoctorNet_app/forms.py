from django import forms
from .models import Solicitacao, ProfissionalSolicitante, CBOs
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class SolicitacaoForm(forms.Form):
    carteirinha_beneficiario = forms.CharField(
        label = 'Número da Carteirinha do Beneficiário', 
        max_length = 8, 
        required = True,
        widget = forms.TextInput(attrs= {
            'placeholder': 'Digite o número da carteirinha',
            'class' : 'form-input'
        })
    )
    nome_profissional = forms.CharField(
        label='Nome do Profissional Solicitante', 
        max_length=100,
        widget = forms.TextInput(attrs= {
            'placeholder': 'Digite o nome do profissional',
            'class' : 'form-input'
        })
    )
    conselho = forms.ChoiceField(
        label='Conselho', 
        choices=ProfissionalSolicitante.Conselho.choices
    )
    UF_Conselho = forms.ChoiceField(
        label='UF', 
        choices=ProfissionalSolicitante.UFConselho.choices
    )
    codigo_conselho = forms.CharField(
        label='Código do Conselho Profissional', 
        max_length=20,
        widget = forms.TextInput(attrs= {
            'placeholder': 'Digite o código do conselho',
            'class' : 'form-input'
        })
    )
    cbos = forms.ModelChoiceField(
        label='CBO-S',
        queryset=CBOs.objects.all(), 
        required=True
    )
    codigo_operadora = forms.CharField(
        label = 'Código do executante', 
        max_length = 10, 
        required = True,
        widget = forms.TextInput(attrs= {
            'placeholder': 'Digite o código do prestador',
            'class' : 'form-input'
        })
    )
    carater_solicitacao = forms.ChoiceField(
        widget = forms.RadioSelect(attrs={'class': 'radio-button'}),
        label = 'Caráter de Solicitação',
        choices = Solicitacao.CaraterSolicitacao.choices
    )
    
    indicacao = forms.CharField(
        label = 'Indicação Clínica', 
        max_length = 500, 
        required = True,
        widget = forms.TextInput(attrs= {
            'placeholder': 'Digite a indicação clínica',
            'class' : 'form-input-indicacao'
    })
    )
    anexos = forms.FileField(
        required = False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        label = 'Envie Arquivos'
        )


class ProcedimentoSolicitadoForm(forms.Form):
    codigo_procedimento = forms.CharField(
        label = 'Código do Procedimento',
        max_length= 8,  
        widget=forms.TextInput(attrs={
            'placeholder': 'Código do procedimento'
        })
    )
    quantidade = forms.IntegerField(
        label= 'Quantidade',
        min_value = 1,
        widget=forms.TextInput(attrs={
            'placeholder': 'Quantidade'
        })
    )

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label = 'Usuário', 
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Usuário'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Senha'
        })
    )
