import re

from django import forms

from .models import ManifestacaoInteresse


class ManifestacaoInteresseForm(forms.ModelForm):
    class Meta:
        model = ManifestacaoInteresse
        fields = ['nome', 'cpf', 'contato', 'curso_interesse', 'cidade', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome', 'autofocus': True}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00', 'inputmode': 'numeric'}),
            'contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone ou e-mail'}),
            'curso_interesse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Técnico em Enfermagem'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade ou bairro (opcional)'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Quer contar mais alguma coisa? (opcional)'}),
        }

    def clean_cpf(self):
        return re.sub(r'\D', '', self.cleaned_data['cpf'])

    def validate_unique(self):
        # O ModelForm normalmente valida sozinho o `unique=True` do CPF e
        # mostraria "já existe" — isso vira um oráculo (dá pra descobrir se o
        # CPF de qualquer pessoa já está cadastrado, testando um por um). A
        # deduplicação é feita de forma silenciosa na view, então aqui a gente
        # não valida unicidade nenhuma.
        pass
