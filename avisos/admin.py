from django.contrib import admin

from .models import Aviso


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publico', 'curso', 'turma', 'autor', 'criado_em', 'email_enviado_para')
    list_filter = ('publico', 'curso', 'turma')
