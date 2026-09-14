from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class EventoCalendarioQuerySet(models.QuerySet):
    def futuros(self):
        hoje = timezone.localdate()
        return self.filter(Q(data_fim__gte=hoje) | Q(data_fim__isnull=True, data_inicio__gte=hoje))

    def passados(self):
        hoje = timezone.localdate()
        return self.filter(Q(data_fim__lt=hoje) | Q(data_fim__isnull=True, data_inicio__lt=hoje))


class EventoCalendario(models.Model):
    class Tipo(models.TextChoices):
        FERIADO = 'feriado', 'Feriado'
        RECESSO = 'recesso', 'Recesso'
        PROVA = 'prova', 'Prova/Avaliação'
        MATRICULA = 'matricula', 'Período de matrícula'
        EVENTO = 'evento', 'Evento'

    titulo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=12, choices=Tipo.choices, default=Tipo.EVENTO)
    data_inicio = models.DateField('Data')
    data_fim = models.DateField(
        'Até', null=True, blank=True, help_text='Deixe em branco se o evento durar só um dia.'
    )
    turma = models.ForeignKey(
        'diario.Turma',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='eventos_calendario',
        help_text='Deixe em branco se o evento valer para toda a escola.',
    )
    descricao = models.TextField(blank=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='eventos_criados'
    )

    objects = EventoCalendarioQuerySet.as_manager()

    class Meta:
        ordering = ['data_inicio']
        verbose_name = 'Evento do calendário'
        verbose_name_plural = 'Eventos do calendário'

    def __str__(self):
        return self.titulo
