from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Usuario

_CAMPOS_ALUNO = ['username', 'first_name', 'last_name', 'email', 'matricula', 'data_nascimento', 'contato_responsavel', 'turma']

_WIDGETS_ALUNO = {
    'username': forms.TextInput(attrs={'class': 'form-control'}),
    'first_name': forms.TextInput(attrs={'class': 'form-control'}),
    'last_name': forms.TextInput(attrs={'class': 'form-control'}),
    'email': forms.EmailInput(attrs={'class': 'form-control'}),
    'matricula': forms.TextInput(attrs={'class': 'form-control'}),
    'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    'contato_responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
    'turma': forms.Select(attrs={'class': 'form-select'}),
}

_LABELS_ALUNO = {
    'username': 'Usuário (login)',
    'first_name': 'Nome',
    'last_name': 'Sobrenome',
    'email': 'E-mail (recebe os avisos da escola)',
}


class AlunoCadastroForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha de acesso', widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = _CAMPOS_ALUNO
        widgets = _WIDGETS_ALUNO
        labels = _LABELS_ALUNO

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('password')
        if senha:
            # Usa os dados já digitados (usuário, nome, e-mail) pra validação de
            # similaridade — a instância do form ainda não tem esses campos aqui.
            aluno_provisorio = Usuario(
                username=cleaned_data.get('username', ''),
                first_name=cleaned_data.get('first_name', ''),
                last_name=cleaned_data.get('last_name', ''),
                email=cleaned_data.get('email', ''),
            )
            try:
                validate_password(senha, aluno_provisorio)
            except ValidationError as erro:
                self.add_error('password', erro)
        return cleaned_data

    def save(self, commit=True):
        aluno = super().save(commit=False)
        aluno.tipo = Usuario.Tipo.ALUNO
        aluno.set_password(self.cleaned_data['password'])
        if commit:
            aluno.save()
        return aluno


class AlunoEdicaoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [c for c in _CAMPOS_ALUNO if c != 'username']
        widgets = _WIDGETS_ALUNO
        labels = _LABELS_ALUNO
