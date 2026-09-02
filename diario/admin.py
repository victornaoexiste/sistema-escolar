from django.contrib import admin

from .models import Aula, Disciplina, Presenca, Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano_letivo')


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class PresencaInline(admin.TabularInline):
    model = Presenca
    extra = 0


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'disciplina', 'professor', 'data')
    list_filter = ('turma', 'disciplina')
    inlines = [PresencaInline]


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ('aula', 'aluno', 'presente')
    list_filter = ('presente',)
