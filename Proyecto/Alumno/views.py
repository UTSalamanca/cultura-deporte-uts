from django.shortcuts import render, redirect
from django.contrib import messages
from Login.decorators import alumno_required
from .models import Club, Horario, Dia, Hora
from .forms import SolicitudForm
from Login.models import UsuarioAcceso
from Sistema.models import Persona, Alumno,AlumnoGrupo, Carrera

@alumno_required
def inicio(request):
    context = obtener_contexto(request)
    return render(request, 'alumno.html')

@alumno_required
def creditos_actuales(request):
    context = obtener_contexto(request)
    return render(request, 'pages/creditos_actuales.html', context)

@alumno_required
def historial_creditos(request):
    context = obtener_contexto(request)
    return render(request, 'pages/historial_creditos.html', context)

@alumno_required
def actividades_culturales(request):
    matricula = request.user.login  
    solicitud_exitosa = False

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            horario = solicitud.id_horario_club
            if horario.capacidad > 0:
                horario.capacidad -= 1
                horario.save()
                solicitud.matricula = matricula
                solicitud.save()
                solicitud_exitosa = True
                messages.success(request, 'Tu solicitud ha sido enviada exitosamente.')
            else:
                messages.error(request, 'El horario seleccionado ya no tiene capacidad.')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')

    else:
        form = SolicitudForm()

    try:
        usuario_acceso = UsuarioAcceso.objects.get(login=request.user)
        persona = Persona.objects.get(cve_persona=usuario_acceso.cve_persona)
        nombre = f"{persona.nombre}"
        apellidos = f"{persona.apellido_paterno} {persona.apellido_materno}"

        alumno = Alumno.objects.get(matricula=matricula)
        alumno_grupo = (
            AlumnoGrupo.objects.filter(matricula=alumno.matricula)
            .select_related('cve_grupo__cve_carrera')
            .order_by('-cve_grupo') 
            .first()  
        )

        if alumno_grupo:
            grupo = alumno_grupo.cve_grupo
            carrera = grupo.cve_carrera
            nombre_carrera = carrera.nombre
            nombre_grupo = grupo.nombre  
        else:
            nombre_carrera = "Grupo no encontrado"
            nombre_grupo = "Grupo no encontrado"

    except UsuarioAcceso.DoesNotExist:
        usuario_acceso = None
        nombre = "Usuario no encontrado"
        apellidos = "Usuario no encontrado"
        nombre_carrera = "Carrera no encontrada"
        nombre_grupo = "Grupo no encontrado"

    except Persona.DoesNotExist:
        persona = None
        nombre = "Persona no asociada"
        apellidos = "Persona no asociada"
        nombre_carrera = "Carrera no asociada"
        nombre_grupo = "Grupo no asociado"

    except Alumno.DoesNotExist:
        nombre_carrera = "Alumno no encontrado"
        nombre_grupo = "Grupo no encontrado"
    except Carrera.DoesNotExist:
        nombre_carrera = "Carrera no asociada"
        nombre_grupo = "Grupo no encontrado"

    # Pasa los datos al contexto
    horarios_disponibles = Horario.objects.filter(capacidad__gt=0)
    clubes = Club.objects.all()
    dias = Dia.objects.all()
    horas = Hora.objects.all()

    context = {
        'form': form,
        'horarios_disponibles': horarios_disponibles,
        'clubes': clubes,
        'dias': dias,
        'horas': horas,
        'nombre': nombre,
        'apellidos': apellidos,
        'matricula': matricula,
        'nombre_carrera': nombre_carrera, 
        'nombre_grupo': nombre_grupo ,
        'solicitud_exitosa': solicitud_exitosa,
    }

    return render(request, 'pages/actividades_culturales.html', context)


@alumno_required
def danza(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/danza.html')

@alumno_required
def voleibol(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/voleibol.html')

@alumno_required
def futbol(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/futbol.html')

@alumno_required
def basquetbol(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/basquetbol.html')

@alumno_required
def taekwondo(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/taekwondo.html')

@alumno_required
def atletismo(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/atletismo.html')

@alumno_required
def artes(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/artes.html')

@alumno_required
def ajedrez(request):
    context = obtener_contexto(request)
    return render(request, 'pages/actividades/ajedrez.html')

def obtener_contexto(request):
    login = request.session.get('login', 'Invitado')
    return {
        'login': login
    }
