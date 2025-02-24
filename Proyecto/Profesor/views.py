import io
from django.shortcuts import redirect, render, get_object_or_404
from Login.decorators import profesor_required
from Alumno.models import Solicitud,  Club, Horario 
from Login.models import UsuarioAcceso
from Sistema.models import Persona, Alumno, AlumnoGrupo
from django.views.decorators.csrf import csrf_exempt
from Profesor.models import ArchivoExcel
from Alumno.models import Horario, Hora, Dia
from Profesor.forms import ArchivoExcelForm
from django.templatetags.static import static
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from io import BytesIO
import os, json
import pandas as pd

@profesor_required
def inicio(request):
    loginuser = request.session.get('loginuser')
    horas = Hora.objects.all()
    dia = Dia.objects.all()


    archivo_path = os.path.join(os.getcwd(), 'Profesor', 'static', 'assets', 'asistencia.xlsx')
    profesor_html = os.path.join(os.getcwd(), 'Profesor', 'templates', 'profesor.html')

    if not os.path.exists(archivo_path):
        raise FileNotFoundError(f"El archivo no se encontró: {archivo_path}")

    
    # SOLICITUD AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        dia = request.GET.get('dia', '')
        excel, cantidad_alumnos = extraer_excel(dia, archivo_path)
        html_stream = io.StringIO(excel)
        tablas = pd.read_html(html_stream)
        print(f'TABLAS: \n {tablas}')
        df = tablas[0]
        return JsonResponse( {'html': excel, 'alumnos': cantidad_alumnos})

    if request.method == 'POST':
        form = ArchivoExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_subido = form.cleaned_data['archivo']

            try:
                archivo_existente = ArchivoExcel.objects.get(usuario=request.user)
                if default_storage.exists(archivo_existente.documento.name):
                    archivo_existente.documento.delete()

                archivo_existente.documento = archivo_subido
                archivo_existente.save()
            except ArchivoExcel.DoesNotExist:
                ArchivoExcel.objects.create(
                    usuario=request.user,
                    documento=archivo_subido
                )

            return render(request, 'profesor.html', {
                'loginuser': loginuser,
                'form': form,
                'message': 'Archivo subido y actualizado correctamente'
            })

    context= {
        'loginuser': loginuser,
        'horas': horas,
        'dias': dia,
        'mapache_docente': static('assets/mapache_docente.jpeg')
    }

    return render(request, 'profesor.html', context)

def solicitudes(request):
    loginuser = request.session.get('loginuser')
    solicitudes = Solicitud.objects.all()
    datos_completos = []
    mensaje_modal = request.session.pop('mensaje_modal', None)  # Tomar y eliminar el mensaje de la sesión

    for solicitud in solicitudes:
        usuario_acceso = UsuarioAcceso.objects.filter(login=solicitud.matricula).first()

        if usuario_acceso:
            persona = Persona.objects.filter(cve_persona=usuario_acceso.cve_persona).first()
            if persona:
                alumno = Alumno.objects.filter(matricula=solicitud.matricula).first()
                if alumno:
                    alumno_grupo = (
                        AlumnoGrupo.objects.filter(matricula=alumno.matricula)
                        .select_related('cve_grupo__cve_carrera')
                        .order_by('-cve_grupo') 
                        .first()
                    )

                    if alumno_grupo:
                        grupo = alumno_grupo.cve_grupo
                        carrera = grupo.cve_carrera
                        nombre_grupo = grupo.nombre
                        nombre_carrera = carrera.nombre
                    else:
                        nombre_grupo = "Grupo no encontrado"
                        nombre_carrera = "Carrera no encontrada"

                    fechaFormateada = solicitud.fecha_inscripcion.strftime('%d/%m/%Y') 

                    datos_completos.append({
                        'matricula': solicitud.matricula,
                        'nombre': f"{persona.nombre} {persona.apellido_paterno} {persona.apellido_materno}",
                        'carrera': nombre_carrera,
                        'grupo': nombre_grupo,
                        'estatus': solicitud.estado,
                        'fecha': fechaFormateada,
                        'id' : solicitud.id_solicitud,
                        'loginuser': loginuser
                    })

    return render(request, 'pages/solicitudes.html', {'datos_completos': datos_completos, 'mensaje_modal': mensaje_modal})


def aceptar_solicitud(request, solicitud_id):
    if request.method == 'POST':
        solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)
        solicitud.estado = 'Aceptada'
        solicitud.save()

        request.session['mensaje_modal'] = 'La solicitud ha sido aceptada.' 
        return redirect('profesor:solicitudes')

def rechazar_solicitud(request, solicitud_id):
    if request.method == 'POST':
        solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)
        solicitud.estado = 'Rechazada'
        solicitud.save()

        request.session['mensaje_modal'] = 'La solicitud ha sido rechazada.'
        return redirect('profesor:solicitudes')

def revertir_solicitud(request, solicitud_id):
    if request.method == 'POST':
        solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)
        solicitud.estado = 'Pendiente'
        solicitud.save()

        request.session['mensaje_modal'] = 'La solicitud ha sido revertida.'  
        return redirect('profesor:solicitudes')
    
def eliminar_solicitud(request, solicitud_id):
    if request.method == 'POST':
        solicitud = get_object_or_404(Solicitud, id_solicitud=solicitud_id)
        solicitud.delete()

        request.session['mensaje_modal'] = 'La solicitud ha sido eliminada.'
        return redirect('profesor:solicitudes')

def extraer_excel(dia, archivo):
    excluir = []
    excluir2 = ['Unnamed: 0']
    dia = dia.upper()
    print(f'dia: {dia}')

    for i in range(1, 31):
        excluir.append(i)

    # OBTENER TABLA DEL EXCEL
    df_alumnos = pd.read_excel(
        archivo,
        sheet_name=dia.upper(),
        header=7,
        index_col=0,
        usecols=lambda col: col not in excluir and col not in excluir2,
    )
    # RENOMBRAR COLUMNAS
    df_alumnos.rename(columns={'Unnamed: 38': 'ESTATUS'}, inplace=True)
    df_alumnos.rename(columns={'T': 'HORAS'}, inplace=True)

    # CONCATENAR COLUMNAS CARRERA, GRUPO Y GRADO
    # OBTENER EL GRADO PARA QUITAR VALORES FLOAT
    df_alumnos['GRADO'] = df_alumnos[['GRADO']].fillna('').astype(str)
    df_alumnos['GRADO'] = df_alumnos['GRADO'].apply(lambda x: x[0] if len(x) > 0 else '')
    df_alumnos['HORAS'] = df_alumnos['HORAS'].fillna(0).astype(int)
    # QUITAR ESPACIOS EN BLANCO A CARRERA 
    df_alumnos['CARRERA'] = df_alumnos['CARRERA'].apply(lambda x: str(x).strip() if isinstance(x, str) else str(x).strip())
    df_alumnos['CARRERA'] = df_alumnos['CARRERA'].apply(lambda x: str(x).upper()) 
    
    # ESTABLECER LOS NOMBRES EN MAYUSCULA
    df_alumnos['NOMBRE(S)'] = df_alumnos['NOMBRE(S)'].apply(lambda  x: str(x).rstrip().upper() if isinstance(x, str) else str(x).rstrip().upper())

    # PARA SOLO MOSTRAR LOS ALUMNOS QUE ESTEN EN EL DOCUMENTO (HASTA DONDE MATRICULA NO ES IGUAL A NaN)
    df_matricula= df_alumnos[['MATRICULA']].fillna(0).astype(int) # ESTABLECE EN CERO LOS VALORES NaN
    df_matricula = df_matricula[df_matricula['MATRICULA'] != 0] # FILTRA TODOS LOS QUE SEAN DIFERENTE DE 0
    df_matricula = df_matricula.loc[df_matricula.index]
    df_info = df_alumnos.loc[df_matricula.index]
    df_alumnos.drop(columns=['MATRICULA'], inplace=True)
    df_info.drop(columns=['MATRICULA'], inplace=True)
    df_info = pd.concat([df_matricula.reset_index(drop=True), df_info.reset_index(drop=True)], axis=1)

    print(df_info)
    # CONCATENA ASISTENCIA Y MATRICULA
    html_table = df_info.to_html(classes='table table-sm table-hover', index=False, escape=False)
    html_table = html_table.replace('<td>', '<td contenteditable="true">')
    cantidad_inscritos = df_info.shape[0]
    

    return html_table, cantidad_inscritos

def guardar_cambios(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            
            archivo_path = os.path.join(os.getcwd(), 'Profesor', 'static', 'assets', 'asistencia.xlsx')
            dia = datos.get('dia')
            dia = dia.upper()

            print(f'archivo: \n {archivo_path}')
            print(f'DIA: \n {dia}')

            df = pd.read_excel(archivo_path, sheet_name=dia, header=7)

            alumnos = datos.get('alumnos', []) 
            print(f'ALUMNOS: \n {alumnos}')

            for fila in alumnos:
                matricula = fila['matricula']
                print(f"Matricula recibida: {matricula}")  # Verifica la matrícula recibida
                row_index = df[df['MATRICULA'] == matricula].index
                print(f"Índice encontrado: {row_index}")  # Verifica si el índice se encuentra
                if not row_index.empty:
                    print(f"Fila encontrada para matrícula {matricula}:")
                    print(df.loc[row_index])  # Imprime la fila que está siendo encontrada
                    df.loc[row_index, 'NOMBRE(S)'] = fila['nombre']
                    df.loc[row_index, 'CARRERA'] = fila['carrera']
                    df.loc[row_index, 'GRADO'] = fila['grado']
                    df.loc[row_index, 'GRUPO'] = fila['grupo']
                    df.loc[row_index, 'HORAS'] = fila['horas']
                    df.loc[row_index, 'ESTATUS'] = fila['estatus']
                    df.loc[row_index, 'SEGUIMIENTO'] = fila['seguimiento']
                else:
                    print(f"No se encontró fila para matrícula {matricula}")


            df.to_excel(archivo_path, index=False)

            # Retornar respuesta JSON
            return JsonResponse({'message': 'Datos guardados correctamente'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@profesor_required
def formulario(request):
    # Renderiza el formulario HTML
    return render(request, 'pages/formulario.html')

def generar_excel(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        cuatrimestre = request.POST['cuatrimestre']
        actividad = request.POST['actividad']
        profesor = request.POST['profesor']
        dia = request.POST['dia']
        horario = request.POST['horario']
        datos = request.POST['datos']

        # Procesar los datos de alumnos
        alumnos = [line.split(",") for line in datos.strip().split("\n")]
        df = pd.DataFrame(alumnos, columns=["MATRICULA", "NOMBRE(S)", "CARRERA", "GRADO", "GRUPO"])

        # Crear el archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Guardar los datos principales
            df.to_excel(writer, sheet_name='Asistencia', index=False)

        # Configurar la respuesta HTTP para descargar el archivo
        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=asistencia_{actividad}.xlsx'
        return response

    # Si no es POST, redirige al formulario
    return redirect('formulario')

@csrf_exempt
def guardar_cambios(request):
    if request.method == "POST":
        data = json.loads(request.body)
        dia = data.get("dia")
        alumnos = data.get("alumnos", [])

        # Procesar los datos recibidos
        for alumno in alumnos:
            matricula = alumno.get("matricula")
            horas = alumno.get("horas")
            estatus = alumno.get("estatus")
            
            # Actualiza la base de datos según la lógica de tu proyecto
            Alumno.objects.filter(matricula=matricula).update(horas=horas, estatus=estatus)
        
        return JsonResponse({"status": "success", "message": "Cambios guardados correctamente."})

    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)
