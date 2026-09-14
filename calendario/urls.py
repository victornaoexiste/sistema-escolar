from django.urls import path

from . import views

app_name = 'calendario'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('novo/', views.novo, name='novo'),
    path('<int:pk>/excluir/', views.excluir, name='excluir'),
]
