from django.conf import settings
from django.db import models


class Curso(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text='Ex: Técnico em Informática')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.nome


class Turma(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='turmas')
    modulo = models.PositiveSmallIntegerField('Módulo', default=1, help_text='Normalmente de 1 a 3')
    identificador = models.CharField(
        'Identificador',
        max_length=5,
        blank=True,
        help_text='Só preencha se houver mais de uma turma no mesmo módulo (ex: A, B)',
    )
    ano_letivo = models.PositiveIntegerField(default=2026)

    class Meta:
        ordering = ['curso__nome', 'modulo', 'identificador']
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

    def __str__(self):
        nome = f'{self.curso} - Módulo {self.modulo}'
        if self.identificador:
            nome += f' {self.identificador}'
        return nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.nome


class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='aulas')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='aulas')
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='aulas_lecionadas',
        limit_choices_to={'tipo': 'professor'},
    )
    data = models.DateField()
    conteudo = models.TextField('Conteúdo ministrado', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data', '-criado_em']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f'{self.turma} · {self.disciplina} · {self.data}'


class Presenca(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='presencas')
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='presencas',
        limit_choices_to={'tipo': 'aluno'},
    )
    presente = models.BooleanField(default=True)

    class Meta:
        unique_together = ('aula', 'aluno')
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'

    def __str__(self):
        situacao = 'presente' if self.presente else 'faltou'
        return f'{self.aluno} — {situacao} em {self.aula}'
