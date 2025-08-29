from django.db import models
from vertical.models.ciudad import VerCiudad
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor

class VerViaje(models.Model):            
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    negocio_id = models.IntegerField(default=0)
    contenedor_id = models.IntegerField()     
    schema_name = models.CharField(max_length=100, null=True)
    usuario_id = models.IntegerField(null=True)
    estado_aceptado = models.BooleanField(default = False)
    ciudad_origen = models.ForeignKey(VerCiudad, on_delete=models.PROTECT, related_name='viajes_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(VerCiudad, on_delete=models.PROTECT, related_name='viajes_ciudad_destino_rel')    
    vehiculo = models.ForeignKey(VerVehiculo, null=True, on_delete=models.PROTECT, related_name='viajes_vehiculo_rel')
    conductor = models.ForeignKey(VerConductor, null=True, on_delete=models.PROTECT, related_name='viajes_conductor_rel')

    class Meta:
        db_table = "ver_viaje"
        ordering = ["-id"]