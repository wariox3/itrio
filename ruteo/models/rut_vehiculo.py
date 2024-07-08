from django.db import models

class RutVehiculo(models.Model):
    placa = models.CharField(max_length=10, null=True)
    capacidad = models.FloatField(default=0)
    
    class Meta:
        db_table = "rut_vehiculo"