from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'profesor'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('solicitudes/',views.solicitudes, name='solicitudes'),
    path('aceptar_solicitud/<int:solicitud_id>/',views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar_solicitud/<int:solicitud_id>/',views.rechazar_solicitud, name='rechazar_solicitud'),
    path('revertir_solicitud/<solicitud_id>/',views.revertir_solicitud, name='revertir_solicitud'),
    path('eliminar_solicitud/<solicitud_id>/ ',views.eliminar_solicitud, name='eliminar_solicitud'),
    path('formulario/', views.formulario, name='formulario'),
    path('generar_excel/', views.generar_excel, name='generar_excel'),
    path("guardar_cambios/", views.guardar_cambios, name="guardar_cambios"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

