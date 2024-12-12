from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name = 'alumno'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('creditos_actuales/', views.creditos_actuales, name='creditos_actuales'),
    path('historial_creditos/', views.historial_creditos,
         name='historial_creditos'),
    path('actividades_culturales/', views.actividades_culturales,
         name="actividades_culturales"),
     path('danza', views.danza,
         name="danza"),
    path('voleibol', views.voleibol,
         name="voleibol"),
    path('futbol', views.futbol,
         name="futbol"),
    path('basquetbol', views.basquetbol,
         name="basquetbol"),
    path('taekwondo', views.taekwondo,
         name="taekwondo"),
    path('atletismo', views.atletismo,
         name="atletismo"),
    path('artes', views.artes,
         name="artes"),
    path('ajedrez', views.ajedrez,
         name="ajedrez"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
