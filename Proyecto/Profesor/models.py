from django.db import models
from Login.models import UsuarioAcceso

class Empleado(models.Model):
    cve_empleado = models.AutoField(primary_key=True)
    cve_persona = models.IntegerField()
    activo = models.BooleanField(default=True)
    cve_unidad_academica = models.IntegerField()

    class Meta:
        managed = False  
        db_table = 'empleado'  
        

    def __str__(self):
        return f'{self.cve_empleado}'
    

class ArchivoExcel(models.Model):
    usuario = models.OneToOneField(
        UsuarioAcceso,
        on_delete=models.CASCADE,
        related_name='archivo_excel'
    )
    documento = models.FileField(upload_to='uploads/')
    
    class Meta:
        managed = False
        db_table = 'archivos_excel'
        verbose_name = 'Acceso Usuario'
        verbose_name_plural = 'Acceso Usuarios'


    def __str__(self):
        return f"Archivo de {self.usuario.username}"
