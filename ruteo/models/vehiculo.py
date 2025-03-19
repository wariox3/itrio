from django.db import models
from ruteo.models.franja import RutFranja

class RutVehiculo(models.Model):
    placa = models.CharField(max_length=10, null=True)
    capacidad = models.FloatField(default=0)
    tiempo = models.FloatField(default=0)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    estado_activo = models.BooleanField(default = False)
    estado_asignado = models.BooleanField(default = False)    
    franja_id = models.IntegerField(null=True)
    franja_codigo = models.CharField(max_length=20, null=True)
    usuario_app = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "rut_vehiculo"