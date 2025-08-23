from django import forms
from .models import Solicitacao

class SolicitacaoForm(forms.ModelForm):
    carteirinha_beneficiario = forms.CharField(label = 'Número da Carteirinha do Beneficiário', max_length = 8, required = True)
    class Meta:
        model = Solicitacao
        fields = ['profissional_solicitante', 'executante', 'procedimento_solicitado', 'carater_solicitacao']