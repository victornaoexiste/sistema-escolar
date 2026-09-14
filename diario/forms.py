from django import forms

from .models import Aula, HorarioAula


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['turma', 'disciplina', 'data', 'conteudo']
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PresencaRapidaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['turma', 'disciplina', 'data']
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class HorarioAulaForm(forms.ModelForm):
    class Meta:
        model = HorarioAula
        fields = ['turma', 'disciplina', 'professor', 'dia_semana', 'hora_inicio', 'hora_fim', 'sala']
        widgets = {
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'professor': forms.Select(attrs={'class': 'form-select'}),
            'dia_semana': forms.Select(attrs={'class': 'form-select'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'sala': forms.TextInput(attrs={'class': 'form-control'}),
        }
