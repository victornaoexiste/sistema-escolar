from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from contas import views as contas_views

urlpatterns = [
    path('', contas_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('contas/', include('contas.urls')),
    path('biblioteca/', include('biblioteca.urls')),
    path('diario/', include('diario.urls')),
    path('avisos/', include('avisos.urls')),
    path('calendario/', include('calendario.urls')),
    path('demanda/', include('demanda.urls')),
]

# Só as capas de livro (arte de capa, baixo risco) ficam públicas em /media/.
# Os PDFs em si (media/livros/) não têm rota pública — só saem pelas views
# autenticadas biblioteca:ler e biblioteca:baixar, mesmo com DEBUG=False
# (necessário pro modo Tailscale Funnel).
urlpatterns += static(settings.MEDIA_URL + 'capas/', document_root=settings.MEDIA_ROOT / 'capas')
