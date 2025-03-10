from django.db import models
from ruteo.models.vehiculo import RutVehiculo

class RutDespacho(models.Model):
    fecha = models.DateTimeField(null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    tiempo = models.FloatField(default=0)
    visitas = models.FloatField(default=0)    
    visitas_entregadas = models.FloatField(default=0)
    estado_aprobado = models.BooleanField(default = False)
    estado_terminado = models.BooleanField(default = False)
    vehiculo = models.ForeignKey(RutVehiculo, null=True, on_delete=models.PROTECT, related_name='despachos_vehiculo_rel')

    class Meta:
        db_table = "rut_despacho"