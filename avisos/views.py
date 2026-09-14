from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from contas.decorators import somente

from .emails import enviar_email_aviso
from .forms import AvisoForm
from .models import Aviso


@login_required
def lista(request):
    usuario = request.user
    avisos = Aviso.objects.select_related('autor', 'curso', 'turma')

    if usuario.is_aluno:
        hoje = timezone.localdate()
        filtro_publico = Q(publico=Aviso.Publico.TODOS)
        if usuario.turma:
            filtro_publico |= Q(publico=Aviso.Publico.TURMA, turma=usuario.turma)
            filtro_publico |= Q(publico=Aviso.Publico.CURSO, curso=usuario.turma.curso)
        avisos = avisos.filter(filtro_publico).filter(Q(expira_em__isnull=True) | Q(expira_em__gte=hoje))

    return render(request, 'avisos/lista.html', {'avisos': avisos})


@somente('admin', 'secretaria', 'professor')
def novo(request):
    if request.method == 'POST':
        form = AvisoForm(request.POST)
        if form.is_valid():
            aviso = form.save(commit=False)
            aviso.autor = request.user
            aviso.save()

            enviados, erro = enviar_email_aviso(aviso)
            aviso.email_enviado_para = enviados
            aviso.save(update_fields=['email_enviado_para'])

            if erro:
                messages.warning(request, f'Aviso publicado, mas o e-mail não pôde ser enviado ({erro}).')
            else:
                messages.success(request, f'Aviso publicado e enviado por e-mail para {enviados} aluno(s).')
            return redirect('avisos:lista')
    else:
        form = AvisoForm()
    return render(request, 'avisos/aviso_form.html', {'form': form, 'titulo': 'Novo aviso'})


@somente('admin', 'secretaria', 'professor')
def excluir(request, pk):
    aviso = get_object_or_404(Aviso, pk=pk)
    if not (request.user.is_admin or request.user.is_secretaria or aviso.autor_id == request.user.pk):
        messages.error(request, 'Você só pode excluir avisos que você mesmo publicou.')
        return redirect('avisos:lista')

    if request.method == 'POST':
        aviso.delete()
        messages.success(request, 'Aviso removido.')
        return redirect('avisos:lista')
    return render(request, 'avisos/aviso_confirmar_exclusao.html', {'aviso': aviso})
