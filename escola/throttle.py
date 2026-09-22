from functools import wraps

from django.core.cache import cache
from django.http import HttpResponse


def _ip_do_cliente(request):
    encaminhado = request.META.get('HTTP_X_FORWARDED_FOR')
    if encaminhado:
        return encaminhado.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'desconhecido')


def limitar_por_ip(nome, max_tentativas, janela_segundos):
    """Limita quantas vezes o mesmo IP pode chamar essa view num período.

    Usa o cache padrão do Django (em memória) — não precisa de nenhum serviço
    externo. Em produção com múltiplos processos, cada processo teria sua
    própria contagem, o que é uma limitação aceitável pro tamanho desse projeto.
    """

    def decorador(view_func):
        @wraps(view_func)
        def view_envolvida(request, *args, **kwargs):
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return view_func(request, *args, **kwargs)

            chave = f'throttle:{nome}:{_ip_do_cliente(request)}'
            try:
                tentativas = cache.incr(chave)
            except ValueError:
                cache.set(chave, 1, timeout=janela_segundos)
                tentativas = 1

            if tentativas > max_tentativas:
                return HttpResponse(
                    'Muitas tentativas. Espere um pouco e tente de novo.',
                    status=429,
                    content_type='text/plain; charset=utf-8',
                )
            return view_func(request, *args, **kwargs)

        return view_envolvida

    return decorador
