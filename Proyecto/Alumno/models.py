from django.db import models
from Profesor.models import Empleado
from Sistema.models import Persona, Usuario, Grupo, AlumnoGrupo


class Hora(models.Model):
    id_hora = models.IntegerField(primary_key=True)  
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()

    class Meta:
        db_table = 'Hora'  
        managed = False   

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_final}"

class Dia(models.Model):
    id_diaSemana = models.IntegerField(primary_key=True)  
    dia = models.CharField(max_length=50)  

    class Meta:
        db_table = 'Dia'  
        managed = False   

    def __str__(self):
        return self.dia  

class Club(models.Model):
    id_club = models.IntegerField(primary_key=True)
    nombre_club = models.CharField(max_length=100)
    cve_empleado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Club'

    def __str__(self):
        return self.nombre_club

    def get_empleado(self):
        return Empleado.objects.using('default').get(cve_empleado=self.cve_empleado)

    def get_persona(self):
        empleado = self.get_empleado()
        return Persona.objects.using('default').get(cve_persona=empleado.cve_persona)
    
class Horario(models.Model):
    id_horario_club = models.IntegerField(primary_key=True)
    id_hora = models.ForeignKey(Hora, on_delete=models.CASCADE, db_column='id_hora')
    id_diaSemana = models.ForeignKey(Dia, on_delete=models.CASCADE, db_column='id_diaSemana')  
    id_club = models.ForeignKey(Club, on_delete=models.CASCADE, db_column='id_club') 
    capacidad = models.IntegerField(default=18)
    ocupado = models.BooleanField(default=False) 

    class Meta:
        managed = False
        db_table = 'Horario'

    def __str__(self):
        return f"{self.id_club.nombre_club} - {self.id_hora.hora_inicio} a {self.id_hora.hora_final}"
    
    def get_nombre_club(self):
        club = Club.objects.using('default').get(id_club=self.id_club)
        return club.nombre_club
    
    def get_hora_inicio(self):
        return self.id_hora.hora_inicio
    
    def get_hora_final(self):
        return self.id_hora.hora_final
    
    def get_capacidad(self):
        return self.capacidad
    
    def get_diaSemana(self):
        dia = Dia.objects.using('default').get(id_diaSemana=self.id_diaSemana)
        return dia.dia


class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_horario_club = models.ForeignKey(Horario, on_delete=models.CASCADE, db_column='id_horario_club')  # Relación con Horario
    matricula = models.IntegerField()  
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    class Meta:
        managed = False
        db_table = 'Solicitud'

    def __str__(self):
        return f"{self.matricula} - {self.estado}"

    def get_nombre_completo(self):
        try:
            usuario = Usuario.objects.using('default').get(login=self.matricula)
            persona = Persona.objects.using('default').get(cve_persona=usuario.cve_persona)
            return f"{persona.nombre} {persona.apellido_paterno} {persona.apellido_materno}"
        except Usuario.DoesNotExist:
            return "Usuario no encontrado"
        except Persona.DoesNotExist:
            return "Persona no encontrada"
        
    def get_nombre_carrera(self):
        try:
            alumno_grupo = AlumnoGrupo.objects.using('default').filter(matricula=self.matricula).first()
            if alumno_grupo:
                grupo = alumno_grupo.cve_grupo  
                return f"{grupo.nombre}"
            else:
                return "Grupo no encontrado"
        except AlumnoGrupo.DoesNotExist:
            return "Grupo no encontrado"
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = self.nuevo_estado
        self.save()
        
