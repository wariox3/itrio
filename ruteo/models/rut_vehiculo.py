from django.db import models

class RutVehiculo(models.Model):
    placa = models.CharField(max_length=10, null=True)
    capacidad = models.FloatField(default=0)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    class Meta:
        db_table = "rut_vehiculo"