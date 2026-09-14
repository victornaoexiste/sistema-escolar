from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from .models import Aviso

Usuario = get_user_model()


def destinatarios_do_aviso(aviso):
    """Alunos que devem receber o aviso, de acordo com o público escolhido."""
    alunos = Usuario.objects.filter(tipo=Usuario.Tipo.ALUNO)
    if aviso.publico == Aviso.Publico.TURMA:
        return alunos.filter(turma=aviso.turma)
    if aviso.publico == Aviso.Publico.CURSO:
        return alunos.filter(turma__curso=aviso.curso)
    return alunos


def enviar_email_aviso(aviso):
    """Envia o aviso por e-mail (em BCC, pra não expor o e-mail dos outros alunos).

    Retorna (quantidade_enviada, erro) — erro é None se deu tudo certo.
    """
    destinatarios = destinatarios_do_aviso(aviso)
    emails = [d.email for d in destinatarios if d.email]
    if not emails:
        return 0, None

    corpo = f'{aviso.corpo}\n\n— {aviso.autor.get_full_name() or aviso.autor.username}, via Vereda'
    mensagem = EmailMessage(
        subject=f'[Aviso] {aviso.titulo}',
        body=corpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[],
        bcc=emails,
    )
    try:
        mensagem.send(fail_silently=False)
    except Exception as erro:  # falha de SMTP não pode derrubar o cadastro do aviso
        return 0, str(erro)
    return len(emails), None
