from django.db import models
from vertical.models.identificacion import VerIdentificacion
from vertical.models.ciudad import VerCiudad
from vertical.models.categoria_licencia import VerCategoriaLicencia

class VerConductor(models.Model):        
    numero_identificacion = models.CharField(max_length=20)
    digito_verificacion = models.CharField(max_length=1, null=True)
    nombre_corto = models.CharField(max_length=200)
    nombre1 = models.CharField(max_length=50, null=True)
    nombre2 = models.CharField(max_length=50, null=True)
    apellido1 = models.CharField(max_length=50, null=True)
    apellido2 = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=100)
    barrio = models.CharField(max_length=200, null=True)
    telefono = models.CharField(max_length=50)
    celular = models.CharField(max_length=50, null=True)
    correo = models.CharField(max_length = 255)
    numero_licencia = models.CharField(max_length=50, null=True)
    fecha_vence_licencia = models.DateField(null=True)
    verificado = models.BooleanField(default = False)
    identificacion = models.ForeignKey(VerIdentificacion, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(VerCiudad, on_delete=models.PROTECT)
    categoria_licencia = models.ForeignKey(VerCategoriaLicencia, on_delete=models.PROTECT)
    
    class Meta:
        db_table = "ver_conductor"
        ordering = ["-id"]