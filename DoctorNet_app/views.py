from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoForm, CustomLoginForm
from .models import Beneficiario, Solicitacao


def loginv(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('autorizacao')
    else:
        form = CustomLoginForm()
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
        form_autorizacao = SolicitacaoForm(request.POST)
        if form_autorizacao.is_valid():
            numero_carteirinha = form.cleaned_data['carteirinha_beneficiario']
            try:
                paciente_encontrado = Beneficiario.objects.get(carteirinha = numero_carteirinha)
                solicitacao = form.save(commit=False)
                solicitacao.beneficiario = paciente_encontrado
                solicitacao.credenciado = request.user 
                solicitacao.save()
                return redirect('detalhe_autorizada', pk=solicitacao.pk)
            except Paciente.DoesNotExist:
                form.add_error('carteirinha_beneficiario', 'Nenhum beneficiário encontrado com este número de carteirinha.')
    else:
        form = SolicitacaoForm()
    return render(request, 'autorizacao.html', {'sol_form': form_autorizacao})

def home(request):
    return render(request,'index.html')

@login_required
def detalhe_autorizada(request, pk):
    solicitacao_obj = get_object_or_404(Solicitacao, pk=pk)
    context = {
        'detalhe_solicitacao': solicitacao_obj
    }
    return render(request, 'detalhe_autorizada.html', context)
