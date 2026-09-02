from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from contas.decorators import somente

from .forms import AulaForm
from .models import Aula, Presenca, Turma

Usuario = get_user_model()


@login_required
def turmas(request):
    usuario = request.user
    if usuario.is_aluno:
        if usuario.turma:
            return redirect('diario:turma', pk=usuario.turma_id)
        messages.info(request, 'Você ainda não está matriculado em nenhuma turma.')
        return redirect('contas:painel')

    todas_turmas = Turma.objects.all()
    return render(request, 'diario/turmas.html', {'turmas': todas_turmas})


@login_required
def turma_diario(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    usuario = request.user

    if usuario.is_aluno and usuario.turma_id != turma.pk:
        messages.error(request, 'Você só pode ver o diário da sua própria turma.')
        return redirect('contas:painel')

    aulas = turma.aulas.select_related('disciplina', 'professor')
    minhas_faltas = None
    if usuario.is_aluno:
        minhas_faltas = Presenca.objects.filter(aluno=usuario, aula__turma=turma, presente=False).count()

    return render(
        request,
        'diario/turma_diario.html',
        {'turma': turma, 'aulas': aulas, 'minhas_faltas': minhas_faltas},
    )


@somente('admin', 'professor')
def nova_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.professor = request.user
            aula.save()
            messages.success(request, 'Aula registrada. Agora marque a presença dos alunos.')
            return redirect('diario:presenca', pk=aula.pk)
    else:
        form = AulaForm()
    return render(request, 'diario/nova_aula.html', {'form': form})


@somente('admin', 'professor')
def presenca(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    alunos = Usuario.objects.filter(tipo=Usuario.Tipo.ALUNO, turma=aula.turma).order_by('first_name', 'username')

    if request.method == 'POST':
        for aluno in alunos:
            presente = request.POST.get(f'presente_{aluno.pk}') == 'on'
            Presenca.objects.update_or_create(aula=aula, aluno=aluno, defaults={'presente': presente})
        messages.success(request, 'Presença salva com sucesso.')
        return redirect('diario:turma', pk=aula.turma_id)

    presencas_atuais = {p.aluno_id: p.presente for p in aula.presencas.all()}
    linhas = [
        {'aluno': aluno, 'presente': presencas_atuais.get(aluno.pk, True)}
        for aluno in alunos
    ]
    return render(request, 'diario/presenca.html', {'aula': aula, 'linhas': linhas})
