from django.conf import settings
from django.db import models


class Aviso(models.Model):
    class Publico(models.TextChoices):
        TODOS = 'todos', 'Toda a escola'
        CURSO = 'curso', 'Um curso específico'
        TURMA = 'turma', 'Uma turma específica'

    titulo = models.CharField(max_length=150)
    corpo = models.TextField('Mensagem')
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='avisos_publicados'
    )
    publico = models.CharField(max_length=10, choices=Publico.choices, default=Publico.TODOS)
    curso = models.ForeignKey(
        'diario.Curso', on_delete=models.CASCADE, null=True, blank=True, related_name='avisos'
    )
    turma = models.ForeignKey(
        'diario.Turma', on_delete=models.CASCADE, null=True, blank=True, related_name='avisos'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateField('Expira em', null=True, blank=True, help_text='Deixe em branco para não expirar.')
    email_enviado_para = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'

    def __str__(self):
        return self.titulo
