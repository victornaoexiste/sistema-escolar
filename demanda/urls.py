from django.urls import path

from . import views

app_name = 'demanda'

urlpatterns = [
    path('', views.nova, name='nova'),
]
