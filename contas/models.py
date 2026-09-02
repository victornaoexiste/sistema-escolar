from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Tipo(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        PROFESSOR = 'professor', 'Professor'
        ALUNO = 'aluno', 'Aluno'

    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.ALUNO)

    # Só usado quando tipo == ALUNO: em qual turma o aluno está matriculado.
    turma = models.ForeignKey(
        'diario.Turma',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='alunos',
        verbose_name='Turma',
    )

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_admin(self):
        return self.tipo == self.Tipo.ADMIN

    @property
    def is_professor(self):
        return self.tipo == self.Tipo.PROFESSOR

    @property
    def is_aluno(self):
        return self.tipo == self.Tipo.ALUNO
