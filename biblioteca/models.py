from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    categoria = models.CharField(max_length=80, blank=True)
    descricao = models.TextField(blank=True)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    arquivo = models.FileField(
        upload_to='livros/',
        validators=[FileExtensionValidator(['pdf'])],
        help_text='Apenas arquivos PDF.',
    )
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='livros_enviados'
    )
    enviado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enviado_em']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        return self.titulo
