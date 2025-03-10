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
    franja = models.ForeignKey(RutFranja, null=True, on_delete=models.PROTECT, related_name='vehiculos_franja_rel')

    class Meta:
        db_table = "rut_vehiculo"