from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'tipo', 'turma', 'is_active')
    list_filter = ('tipo', 'turma', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Dados escolares', {'fields': ('tipo', 'turma')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados escolares', {'fields': ('tipo', 'turma')}),
    )
