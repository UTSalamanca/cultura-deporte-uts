from django.shortcuts import render, redirect
from Alumno.models import Solicitud, Horario, Dia, Club
from Sistema.models import Persona, Usuario


# Create your views here.

def inicio(request):
    return redirect('administrador:creditos')

def creditos(request):
    selected_club = request.GET.get('club', '')
    solicitudes = Solicitud.objects.filter(estado='Aceptada') 

    if selected_club:  
        solicitudes = solicitudes.filter(id_horario_club__id_club__nombre_club=selected_club)

    solicitudes = [
        {
            'solicitud': solicitud,
            'nombre_completo': solicitud.get_nombre_completo(),
            'grupo': solicitud.get_nombre_carrera(),
           
        }
        for solicitud in solicitudes
    ]

    return render(request, 'pages/creditos.html', {
        'selected_club': selected_club,
        'solicitudes': solicitudes,
        
    })

def carta_laboral(request):
    return render(request, 'pages/carta_laboral.html')


