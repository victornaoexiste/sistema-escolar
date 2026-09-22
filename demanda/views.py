from django.contrib import messages
from django.shortcuts import redirect, render

from escola.throttle import limitar_por_ip

from .forms import ManifestacaoInteresseForm
from .models import ManifestacaoInteresse


@limitar_por_ip('demanda', max_tentativas=5, janela_segundos=3600)
def nova(request):
    if request.method == 'POST':
        form = ManifestacaoInteresseForm(request.POST)
        if form.is_valid():
            # Se o CPF já existe, não salvamos de novo — mas mostramos a mesma
            # mensagem de sempre, pra não dar pra descobrir por tentativa e
            # erro se um CPF de terceiro já está cadastrado.
            if not ManifestacaoInteresse.objects.filter(cpf=form.cleaned_data['cpf']).exists():
                form.save()
            messages.success(
                request,
                'Recebemos seu interesse! Obrigado por participar do levantamento de demanda.',
            )
            return redirect('demanda:nova')
    else:
        form = ManifestacaoInteresseForm()
    return render(request, 'demanda/nova.html', {'form': form})
