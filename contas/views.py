from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class TelaLogin(auth_views.LoginView):
    template_name = 'contas/login.html'
    redirect_authenticated_user = True


@login_required
def painel(request):
    usuario = request.user

    if usuario.is_admin:
        return render(request, 'contas/painel_admin.html')

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
