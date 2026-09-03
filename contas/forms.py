from django import forms

from .models import Usuario

_CAMPOS_ALUNO = ['username', 'first_name', 'last_name', 'matricula', 'data_nascimento', 'contato_responsavel', 'turma']

_WIDGETS_ALUNO = {
    'username': forms.TextInput(attrs={'class': 'form-control'}),
    'first_name': forms.TextInput(attrs={'class': 'form-control'}),
    'last_name': forms.TextInput(attrs={'class': 'form-control'}),
    'matricula': forms.TextInput(attrs={'class': 'form-control'}),
    'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    'contato_responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
    'turma': forms.Select(attrs={'class': 'form-select'}),
}

_LABELS_ALUNO = {
    'username': 'Usuário (login)',
    'first_name': 'Nome',
    'last_name': 'Sobrenome',
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
