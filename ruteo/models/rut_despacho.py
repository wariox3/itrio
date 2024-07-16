from django.db import models
from ruteo.models.rut_vehiculo import RutVehiculo

class RutDespacho(models.Model):
    fecha = models.DateTimeField(null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    visitas = models.FloatField(default=0)
    vehiculo = models.ForeignKey(RutVehiculo, null=True, on_delete=models.PROTECT, related_name='despachos_vehiculo_rel')

    class Meta:
        db_table = "rut_despacho"