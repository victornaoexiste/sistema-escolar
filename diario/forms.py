from django import forms

from .models import Aula


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
