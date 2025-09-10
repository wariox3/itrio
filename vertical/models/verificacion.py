from django.db import models
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor

class VerVerificacion(models.Model):        
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)    
    verificador = models.CharField(max_length=100, null=True)
    vehiculo = models.ForeignKey(VerVehiculo, null=True, on_delete=models.PROTECT, related_name='verificaciones_vehiculo_rel')
    conductor = models.ForeignKey(VerConductor, null=True, on_delete=models.PROTECT, related_name='verificaciones_conductor_rel')    
    
    class Meta:
        db_table = "ver_verificacion"
        ordering = ["-id"]