from django.urls import path

from . import views

app_name = 'diario'

urlpatterns = [
    path('', views.turmas, name='turmas'),
    path('aula/nova/', views.nova_aula, name='nova_aula'),
    path('presenca/rapida/', views.presenca_rapida, name='presenca_rapida'),
    path('aula/<int:pk>/presenca/', views.presenca, name='presenca'),
    path('turma/<int:pk>/', views.turma_diario, name='turma'),
    path('turma/<int:pk>/frequencia/', views.frequencia_turma, name='frequencia_turma'),
    path('horarios/', views.horarios, name='horarios'),
    path('horarios/novo/', views.horario_novo, name='horario_novo'),
    path('horarios/<int:pk>/excluir/', views.horario_excluir, name='horario_excluir'),
]
