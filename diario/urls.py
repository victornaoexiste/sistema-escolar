from django.urls import path

from . import views

app_name = 'diario'

urlpatterns = [
    path('', views.turmas, name='turmas'),
    path('aula/nova/', views.nova_aula, name='nova_aula'),
    path('aula/<int:pk>/presenca/', views.presenca, name='presenca'),
    path('turma/<int:pk>/', views.turma_diario, name='turma'),
]
