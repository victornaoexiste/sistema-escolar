import itertools

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contas.decorators import somente

from .forms import EventoCalendarioForm
from .models import EventoCalendario

MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
    7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}


def _agrupar_por_mes(eventos, ordem_decrescente=False):
    grupos = []
    chave = lambda e: (e.data_inicio.year, e.data_inicio.month)  # noqa: E731
    for (ano, mes), eventos_do_mes in itertools.groupby(eventos, key=chave):
        grupos.append({'rotulo': f'{MESES_PT[mes]} de {ano}', 'eventos': list(eventos_do_mes)})
    return grupos


@login_required
def lista(request):
    usuario = request.user
    mostrar_passados = request.GET.get('passados') == '1'

    eventos = EventoCalendario.objects.select_related('turma')
    if usuario.is_aluno:
        filtro = Q(turma__isnull=True)
        if usuario.turma:
            filtro |= Q(turma=usuario.turma)
        eventos = eventos.filter(filtro)

    eventos = eventos.passados() if mostrar_passados else eventos.futuros()
    ordenacao = '-data_inicio' if mostrar_passados else 'data_inicio'
    grupos = _agrupar_por_mes(eventos.order_by(ordenacao))

    return render(request, 'calendario/lista.html', {'grupos': grupos, 'mostrar_passados': mostrar_passados})


@somente('admin', 'secretaria')
def novo(request):
    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.criado_por = request.user
            evento.save()
            messages.success(request, 'Evento adicionado ao calendário.')
            return redirect('calendario:lista')
    else:
        form = EventoCalendarioForm()
    return render(request, 'calendario/evento_form.html', {'form': form, 'titulo': 'Novo evento'})


@somente('admin', 'secretaria')
def excluir(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento removido.')
        return redirect('calendario:lista')
    return render(request, 'calendario/evento_confirmar_exclusao.html', {'evento': evento})
