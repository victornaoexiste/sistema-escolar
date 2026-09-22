from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from contas.decorators import somente

from .forms import AulaForm, HorarioAulaForm, PresencaRapidaForm
from .frequencia import frequencia_por_disciplina, frequencia_turma_por_aluno
from .models import Aula, HorarioAula, Presenca, Turma

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
    minha_frequencia = None
    if usuario.is_aluno:
        minha_frequencia = frequencia_por_disciplina(turma, usuario)

    return render(
        request,
        'diario/turma_diario.html',
        {'turma': turma, 'aulas': aulas, 'minha_frequencia': minha_frequencia},
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
def presenca_rapida(request):
    if request.method == 'POST':
        form = PresencaRapidaForm(request.POST)
        if form.is_valid():
            aula, _ = Aula.objects.get_or_create(
                turma=form.cleaned_data['turma'],
                disciplina=form.cleaned_data['disciplina'],
                data=form.cleaned_data['data'],
                defaults={'professor': request.user, 'conteudo': ''},
            )
            return redirect('diario:presenca', pk=aula.pk)
    else:
        form = PresencaRapidaForm()
    return render(request, 'diario/presenca_rapida.html', {'form': form})


@somente('admin', 'professor', 'secretaria')
def presenca(request, pk):
    aula = get_object_or_404(Aula, pk=pk)

    if request.user.is_professor and aula.professor_id != request.user.id:
        messages.error(request, 'Você só pode alterar a presença das próprias aulas.')
        return redirect('contas:painel')

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


@login_required
def horarios(request):
    usuario = request.user
    turmas_disponiveis = None

    if usuario.is_aluno:
        if not usuario.turma:
            messages.info(request, 'Você ainda não está matriculado em nenhuma turma.')
            return redirect('contas:painel')
        turma = usuario.turma
    else:
        turmas_disponiveis = Turma.objects.all()
        turma_id = request.GET.get('turma') or (turmas_disponiveis.first().pk if turmas_disponiveis else None)
        turma = get_object_or_404(Turma, pk=turma_id) if turma_id else None

    if not turma:
        return render(request, 'diario/horarios.html', {'turma': None, 'turmas_disponiveis': turmas_disponiveis})

    todos_horarios = turma.horarios.select_related('disciplina', 'professor')
    hoje = timezone.localdate()
    horarios_hoje = todos_horarios.filter(dia_semana=hoje.weekday())

    grade_por_dia = {dia: [] for dia, _ in HorarioAula.DiaSemana.choices}
    for horario in todos_horarios:
        grade_por_dia[horario.dia_semana].append(horario)
    grade = [(rotulo, grade_por_dia[dia]) for dia, rotulo in HorarioAula.DiaSemana.choices]

    return render(
        request,
        'diario/horarios.html',
        {
            'turma': turma,
            'turmas_disponiveis': turmas_disponiveis,
            'horarios_hoje': horarios_hoje,
            'grade': grade,
        },
    )


@somente('admin', 'secretaria', 'professor')
def frequencia_turma(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    linhas = frequencia_turma_por_aluno(turma)
    return render(request, 'diario/frequencia_turma.html', {'turma': turma, 'linhas': linhas})


@somente('admin', 'secretaria')
def horario_novo(request):
    if request.method == 'POST':
        form = HorarioAulaForm(request.POST)
        if form.is_valid():
            horario = form.save()
            messages.success(request, 'Horário cadastrado com sucesso.')
            return redirect(f"{reverse('diario:horarios')}?turma={horario.turma_id}")
    else:
        form = HorarioAulaForm()
    return render(request, 'diario/horario_form.html', {'form': form, 'titulo': 'Novo horário de aula'})


@somente('admin', 'secretaria')
def horario_excluir(request, pk):
    horario = get_object_or_404(HorarioAula, pk=pk)
    turma_id = horario.turma_id
    if request.method == 'POST':
        horario.delete()
        messages.success(request, 'Horário removido.')
        return redirect(f"{reverse('diario:horarios')}?turma={turma_id}")
    return render(request, 'diario/horario_confirmar_exclusao.html', {'horario': horario})
