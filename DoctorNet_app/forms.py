from django import forms
from .models import Solicitacao
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class SolicitacaoForm(forms.ModelForm):
    carteirinha_beneficiario = forms.CharField(label = 'Número da Carteirinha do Beneficiário', max_length = 8, required = True)
    class Meta:
        model = Solicitacao
        fields = ['profissional_solicitante', 'executante', 'procedimento_solicitado', 'carater_solicitacao']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label = 'Usuário', widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Nome de usuário'
        }))
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Senha'
        })
    )