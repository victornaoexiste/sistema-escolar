from django import forms

from .models import Aviso


class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ['titulo', 'corpo', 'publico', 'curso', 'turma', 'expira_em']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'corpo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'publico': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'expira_em': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        dados = super().clean()
        publico = dados.get('publico')
        if publico == Aviso.Publico.CURSO and not dados.get('curso'):
            self.add_error('curso', 'Escolha um curso quando o público for "Um curso específico".')
        if publico == Aviso.Publico.TURMA and not dados.get('turma'):
            self.add_error('turma', 'Escolha uma turma quando o público for "Uma turma específica".')
        return dados
