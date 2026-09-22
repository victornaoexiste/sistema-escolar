from django.db import models

from .validators import validar_cpf


class ManifestacaoInteresse(models.Model):
    nome = models.CharField('Nome', max_length=150)
    cpf = models.CharField('CPF', max_length=14, unique=True, validators=[validar_cpf])
    contato = models.CharField('Telefone ou e-mail', max_length=150)
    curso_interesse = models.CharField('Curso técnico de interesse', max_length=150)
    cidade = models.CharField('Cidade / bairro', max_length=150, blank=True)
    mensagem = models.TextField('Mensagem (opcional)', blank=True)
    criado_em = models.DateTimeField('Recebido em', auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Manifestação de interesse'
        verbose_name_plural = 'Levantamento de demanda'

    def __str__(self):
        return f'{self.nome} — {self.curso_interesse}'
