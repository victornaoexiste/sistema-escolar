from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import somente
from .forms import AlunoCadastroForm, AlunoEdicaoForm
from .models import Usuario


class TelaLogin(auth_views.LoginView):
    template_name = 'contas/login.html'
    redirect_authenticated_user = True


@login_required
def painel(request):
    usuario = request.user

    if usuario.is_admin:
        return render(request, 'contas/painel_admin.html')

    if usuario.is_secretaria:
        alunos_count = Usuario.objects.filter(tipo=Usuario.Tipo.ALUNO).count()
        return render(request, 'contas/painel_secretaria.html', {'alunos_count': alunos_count})

    if usuario.is_professor:
        from diario.models import Aula

        aulas = Aula.objects.filter(professor=usuario).order_by('-data')[:5]
        return render(request, 'contas/painel_professor.html', {'aulas': aulas})

    from diario.models import Aula
    from biblioteca.models import Livro

    aulas = []
    if usuario.turma:
        aulas = Aula.objects.filter(turma=usuario.turma).order_by('-data')[:5]
    livros = Livro.objects.order_by('-enviado_em')[:5]
    return render(request, 'contas/painel_aluno.html', {'aulas': aulas, 'livros': livros})


@somente('admin', 'secretaria')
def alunos_lista(request):
    termo = request.GET.get('q', '').strip()
    alunos = Usuario.objects.filter(tipo=Usuario.Tipo.ALUNO).select_related('turma')
    if termo:
        alunos = alunos.filter(first_name__icontains=termo) | alunos.filter(
            last_name__icontains=termo
        ) | alunos.filter(matricula__icontains=termo)
    alunos = alunos.order_by('first_name', 'username')
    return render(request, 'contas/alunos_lista.html', {'alunos': alunos, 'termo': termo})


@somente('admin', 'secretaria')
def aluno_novo(request):
    if request.method == 'POST':
        form = AlunoCadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno cadastrado com sucesso.')
            return redirect('contas:alunos_lista')
    else:
        form = AlunoCadastroForm()
    return render(request, 'contas/aluno_form.html', {'form': form, 'titulo': 'Cadastrar aluno'})


@somente('admin', 'secretaria')
def aluno_editar(request, pk):
    aluno = get_object_or_404(Usuario, pk=pk, tipo=Usuario.Tipo.ALUNO)
    if request.method == 'POST':
        form = AlunoEdicaoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do aluno atualizados.')
            return redirect('contas:alunos_lista')
    else:
        form = AlunoEdicaoForm(instance=aluno)
    return render(request, 'contas/aluno_form.html', {'form': form, 'titulo': f'Editar aluno — {aluno}'})
