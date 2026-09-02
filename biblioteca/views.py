from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from contas.decorators import somente

from .forms import LivroForm
from .models import Livro


@login_required
def lista(request):
    termo = request.GET.get('q', '').strip()
    livros = Livro.objects.all()
    if termo:
        livros = livros.filter(titulo__icontains=termo) | livros.filter(autor__icontains=termo) | livros.filter(
            categoria__icontains=termo
        )
    return render(request, 'biblioteca/lista.html', {'livros': livros, 'termo': termo})


@login_required
def detalhe(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'biblioteca/detalhe.html', {'livro': livro})


@login_required
def baixar(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return FileResponse(livro.arquivo.open('rb'), as_attachment=True, filename=f'{livro.titulo}.pdf')


@somente('admin', 'professor')
def enviar(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.enviado_por = request.user
            livro.save()
            messages.success(request, f'Livro "{livro.titulo}" enviado com sucesso.')
            return redirect('biblioteca:detalhe', pk=livro.pk)
    else:
        form = LivroForm()
    return render(request, 'biblioteca/enviar.html', {'form': form})
