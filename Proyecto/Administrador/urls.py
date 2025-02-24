from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('creditos/', views.creditos, name='creditos'),
    path('carta_laboral/', views.carta_laboral, name='carta_laboral'),
]
