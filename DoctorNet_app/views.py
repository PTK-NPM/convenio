from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoForm
from .models import Beneficiario, Solicitacao


def loginv(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('autorizacao')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form})

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('autorizacao')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form_cadastro': form})

@login_required
def sol_autorizacao(request):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            numero_carteirinha = form.cleaned_data['carteirinha_beneficiario']
            try:
                paciente_encontrado = Beneficiario.objects.get(carteirinha = numero_carteirinha)
            except:
                pass
    return render(request, 'autorizacao.html')

def home(request):
    return render(request,'index.html')