from django.urls import path

from . import views

app_name = 'biblioteca'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('enviar/', views.enviar, name='enviar'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('<int:pk>/baixar/', views.baixar, name='baixar'),
]
