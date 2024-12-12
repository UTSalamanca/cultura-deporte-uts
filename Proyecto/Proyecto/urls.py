from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Login.urls')),
    path('profesor/', include('Profesor.urls', namespace='profesor')),
    path('alumno/', include('Alumno.urls', namespace='alumno')),
    path('administrador/', include('Administrador.urls', namespace='administrador')),
]
