from django.db import models
from general.models.rh import GenRh
from general.models.ciudad import GenCiudad
from general.models.identificacion import GenIdentificacion

class TteConductor(models.Model):    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField()
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
    numero_licencia = models.CharField(max_length=50)
    categoria_licencia = models.CharField(max_length=2)
    fecha_vence_licencia = models.DateField()
    fecha_expedicion_licencia = models.DateField()
    fecha_ingreso = models.DateField(null=True)
    fecha_retiro = models.DateField(null=True)
    propio = models.BooleanField(default = False)
    estado_inactivo = models.BooleanField(default = False)
    estado_revisado = models.BooleanField(default = False)
    comentario = models.CharField(max_length=500, null=True)
    identificacion = models.ForeignKey(GenIdentificacion, on_delete=models.PROTECT, related_name='conductores_identificacion_rel')
    ciudad = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='conductores_ciudad_rel')
    rh = models.ForeignKey(GenRh, on_delete=models.PROTECT, related_name='conductores_rh_rel')

    class Meta:
        db_table = "tte_conductor"
        ordering = ["-id"]