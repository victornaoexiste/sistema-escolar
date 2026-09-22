from django.contrib import admin

from .models import ManifestacaoInteresse


@admin.register(ManifestacaoInteresse)
class ManifestacaoInteresseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'curso_interesse', 'cidade', 'contato', 'criado_em')
    list_filter = ('curso_interesse', 'cidade')
    search_fields = ('nome', 'cpf', 'curso_interesse', 'contato', 'cidade')
    ordering = ('-criado_em',)
