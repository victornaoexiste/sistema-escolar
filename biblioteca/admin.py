from django.contrib import admin

from .models import Livro


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'enviado_por', 'enviado_em')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'autor')
