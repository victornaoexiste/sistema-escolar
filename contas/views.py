from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator

from escola.throttle import limitar_por_ip

from .decorators import somente
from .documentos import gerar_declaracao_matricula, gerar_extrato_frequencia
from .forms import AlunoCadastroForm, AlunoEdicaoForm
from .models import Usuario


@method_decorator(limitar_por_ip('login', max_tentativas=10, janela_segundos=900), name='post')
class TelaLogin(auth_views.LoginView):
    template_name = 'contas/login.html'
    redirect_authenticated_user = True


def home(request):
    if request.user.is_authenticated:
        return redirect('contas:painel')
    return render(request, 'contas/home.html')


@login_required
def painel(request):
    usuario = request.user

    if usuario.is_admin or usuario.is_secretaria:
        from django.db.models import Count
        from django.utils import timezone

        from avisos.models import Aviso
        from biblioteca.models import Livro
        from calendario.models import EventoCalendario
        from diario.frequencia import alunos_em_risco_por_turma
        from diario.models import Aula, HorarioAula, Turma

        alunos_count = Usuario.objects.filter(tipo=Usuario.Tipo.ALUNO).count()
        turmas_em_risco = alunos_em_risco_por_turma()
        turmas = Turma.objects.annotate(num_alunos=Count('alunos')).select_related('curso')
        proximos_eventos = EventoCalendario.objects.futuros()[:5]
        avisos_recentes = Aviso.objects.order_by('-criado_em')[:6]
        livros_recentes = Livro.objects.order_by('-enviado_em')[:6]
        aulas_recentes = Aula.objects.select_related('turma', 'disciplina').order_by('-data', '-criado_em')[:6]
        hoje = timezone.localdate()
        horarios_hoje = HorarioAula.objects.filter(dia_semana=hoje.weekday()).select_related(
            'turma', 'disciplina'
        ).order_by('hora_inicio')[:8]
        contexto = {
            'alunos_count': alunos_count,
            'turmas_em_risco': turmas_em_risco,
            'turmas': turmas,
            'proximos_eventos': proximos_eventos,
            'avisos_recentes': avisos_recentes,
            'livros_recentes': livros_recentes,
            'aulas_recentes': aulas_recentes,
            'horarios_hoje': horarios_hoje,
        }

        if usuario.is_admin:
            return render(request, 'contas/painel_admin.html', contexto)
        return render(request, 'contas/painel_secretaria.html', contexto)

    if usuario.is_professor:
        from django.utils import timezone

        from avisos.models import Aviso
        from biblioteca.models import Livro
        from calendario.models import EventoCalendario
        from diario.models import Aula, HorarioAula

        aulas = Aula.objects.filter(professor=usuario).order_by('-data')[:6]
        hoje = timezone.localdate()
        horarios_hoje = HorarioAula.objects.filter(
            professor=usuario, dia_semana=hoje.weekday()
        ).select_related('turma', 'disciplina').order_by('hora_inicio')
        avisos_recentes = Aviso.objects.order_by('-criado_em')[:6]
        livros_recentes = Livro.objects.order_by('-enviado_em')[:6]
        proximos_eventos = EventoCalendario.objects.futuros()[:5]
        return render(
            request,
            'contas/painel_professor.html',
            {
                'aulas': aulas,
                'horarios_hoje': horarios_hoje,
                'avisos_recentes': avisos_recentes,
                'livros_recentes': livros_recentes,
                'proximos_eventos': proximos_eventos,
            },
        )

    from django.db.models import Q
    from django.utils import timezone

    from avisos.models import Aviso
    from biblioteca.models import Livro
    from calendario.models import EventoCalendario
    from diario.frequencia import frequencia_geral
    from diario.models import Aula

    aulas = []
    horarios_hoje = []
    minha_frequencia_geral = None
    if usuario.turma:
        aulas = Aula.objects.filter(turma=usuario.turma).order_by('-data')[:5]
        hoje = timezone.localdate()
        horarios_hoje = usuario.turma.horarios.filter(dia_semana=hoje.weekday()).select_related('disciplina', 'professor')
        minha_frequencia_geral = frequencia_geral(usuario.turma, usuario)

    livros = Livro.objects.order_by('-enviado_em')[:5]

    filtro_avisos = Q(publico=Aviso.Publico.TODOS)
    filtro_eventos = Q(turma__isnull=True)
    if usuario.turma:
        filtro_avisos |= Q(publico=Aviso.Publico.TURMA, turma=usuario.turma)
        filtro_avisos |= Q(publico=Aviso.Publico.CURSO, curso=usuario.turma.curso)
        filtro_eventos |= Q(turma=usuario.turma)
    avisos_recentes = Aviso.objects.filter(filtro_avisos).order_by('-criado_em')[:5]
    proximos_eventos = EventoCalendario.objects.futuros().filter(filtro_eventos)[:5]

    return render(
        request,
        'contas/painel_aluno.html',
        {
            'aulas': aulas,
            'livros': livros,
            'horarios_hoje': horarios_hoje,
            'avisos_recentes': avisos_recentes,
            'minha_frequencia_geral': minha_frequencia_geral,
            'proximos_eventos': proximos_eventos,
        },
    )


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


def _resolver_aluno_documento(request, pk):
    """Aluno só gera o próprio documento; admin/secretaria podem gerar de qualquer aluno."""
    if pk is not None:
        if not (request.user.is_admin or request.user.is_secretaria):
            return None
        return get_object_or_404(Usuario, pk=pk, tipo=Usuario.Tipo.ALUNO)
    if request.user.is_aluno:
        return request.user
    return None


@login_required
def documentos(request):
    if not request.user.is_aluno:
        messages.error(request, 'Essa página é só para alunos. Gere documentos de um aluno pela lista de Alunos.')
        return redirect('contas:painel')
    return render(request, 'contas/documentos.html')


@login_required
def documento_declaracao(request, pk=None):
    aluno = _resolver_aluno_documento(request, pk)
    if aluno is None:
        messages.error(request, 'Você não tem permissão para gerar esse documento.')
        return redirect('contas:painel')
    if not aluno.turma:
        messages.error(request, f'{aluno.get_full_name() or aluno.username} não está matriculado(a) em nenhuma turma ainda.')
        return redirect('contas:alunos_lista' if pk else 'contas:painel')

    pdf = gerar_declaracao_matricula(aluno)
    resposta = HttpResponse(pdf, content_type='application/pdf')
    resposta['Content-Disposition'] = f'inline; filename="declaracao_matricula_{aluno.username}.pdf"'
    return resposta


@login_required
def documento_frequencia(request, pk=None):
    aluno = _resolver_aluno_documento(request, pk)
    if aluno is None:
        messages.error(request, 'Você não tem permissão para gerar esse documento.')
        return redirect('contas:painel')
    if not aluno.turma:
        messages.error(request, f'{aluno.get_full_name() or aluno.username} não está matriculado(a) em nenhuma turma ainda.')
        return redirect('contas:alunos_lista' if pk else 'contas:painel')

    pdf = gerar_extrato_frequencia(aluno)
    resposta = HttpResponse(pdf, content_type='application/pdf')
    resposta['Content-Disposition'] = f'inline; filename="extrato_frequencia_{aluno.username}.pdf"'
    return resposta


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
