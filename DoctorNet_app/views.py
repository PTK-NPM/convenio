from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoForm, CustomLoginForm, ProcedimentoSolicitadoForm
from .models import Beneficiario, Solicitacao, Executante, Procedimento, ProfissionalSolicitante, ItemSolicitacao


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

ProcedimentoFormSet = formset_factory(ProcedimentoSolicitadoForm, extra=1)

@login_required
def sol_autorizacao(request):
    if request.method == 'POST':
        form = SolicitacaoForm(request.POST)
        formset= ProcedimentoFormSet(request.POST, prefix='procedimentos')
        if form.is_valid() and formset.is_valid():
            numero_carteirinha = form.cleaned_data['carteirinha_beneficiario']
            codigo_executante = form.cleaned_data['codigo_operadora']
            codigo_conselho = form.cleaned_data['codigo_conselho']
            
            defaults_profissional = {
                'nome_profissional': form.cleaned_data['nome_profissional'],
                'tipo_conselho': form.cleaned_data['conselho'],
                'UF_Conselho': form.cleaned_data['UF_Conselho'],
                'cbos': form.cleaned_data['cbos']
            }
            profissional_obj, created = ProfissionalSolicitante.objects.get_or_create(
                codigo = codigo_conselho,
                defaults = defaults_profissional
            )
            try:
                paciente_encontrado = Beneficiario.objects.get(carteirinha = numero_carteirinha)
                executante_encontrado = Executante.objects.get(codigo = codigo_executante)
                nova_solicitacao = Solicitacao.objects.create(
                paciente = paciente_encontrado,
                profissional_solicitante = profissional_obj,
                executante = executante_encontrado,
                credenciado = request.user,
                carater_solicitacao = form.cleaned_data['carater_solicitacao']
                indicacao = form.cleaned_data['indicacao']
            )
                for form_procedimento in formset:
                    if form_procedimento.has_changed():
                        procedimento_codigo = form_procedimento.cleaned_data['codigo_procedimento']
                        quantidade_solicitada = form_procedimento.cleaned_data['quantidade']
                            
                        try:
                            procedimento_encontrado = Procedimento.objects.get(codigo_procedimento=procedimento_codigo)
                                
                            ItemSolicitacao.objects.create(
                                solicitacao=nova_solicitacao,
                                procedimento=procedimento_encontrado,
                                quantidade=quantidade_solicitada)
                            
                        except Procedimento.DoesNotExist:
                                form_procedimento.add_error('codigo_procedimento', 'Código de procedimento inválido.')

                return redirect('detalhes_autorizada', id=nova_solicitacao.pk)
            except Beneficiario.DoesNotExist:
                form.add_error('carteirinha_beneficiario', 'Nenhum beneficiário encontrado com este número de carteirinha.')
            except Executante.DoesNotExist:
                form.add_error('codigo_operadora', 'Nenhum executante encontrado.')
            except Procedimento.DoesNotExist:
                form.add_error('procedimento', 'Nenhum procedimento encontrado.')

            
    else:
        form = SolicitacaoForm()
        formset = ProcedimentoFormSet(prefix='procedimentos')
    return render(request, 'autorizacao.html', {'sol_form': form, 'formset': formset})

def home(request):
    return render(request,'index.html')

@login_required
def detalhes_autorizada(request, id):
    solicitacao_obj = get_object_or_404(Solicitacao, pk=id)
    context = {
        'detalhes_autorizada': solicitacao_obj
    }
    return render(request, 'detalhes_autorizada.html', context)
