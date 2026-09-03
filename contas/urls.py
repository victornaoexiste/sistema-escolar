from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'contas'

urlpatterns = [
    path('login/', views.TelaLogin.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('painel/', views.painel, name='painel'),
    path('alunos/', views.alunos_lista, name='alunos_lista'),
    path('alunos/novo/', views.aluno_novo, name='aluno_novo'),
    path('alunos/<int:pk>/editar/', views.aluno_editar, name='aluno_editar'),
]
