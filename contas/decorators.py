from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def somente(*tipos_permitidos):
    """Restringe a view aos tipos de usuário informados (ex: 'admin', 'professor')."""

    def decorador(view_func):
        @wraps(view_func)
        @login_required
        def view_envolvida(request, *args, **kwargs):
            if request.user.tipo not in tipos_permitidos:
                messages.error(request, 'Você não tem permissão para acessar essa página.')
                return redirect('contas:painel')
            return view_func(request, *args, **kwargs)

        return view_envolvida

    return decorador
