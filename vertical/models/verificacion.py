from django.db import models
from vertical.models.vehiculo import VerVehiculo
from vertical.models.conductor import VerConductor
from seguridad.models import User

class VerVerificacion(models.Model):        
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    fecha_verificacion = models.DateTimeField(null=True)
    fecha_verificacion_vence = models.DateTimeField(null=True)
    verificacion_tipo_id = models.IntegerField()    
    estado_proceso = models.BooleanField(default = False)
    verificado = models.BooleanField(default = False)
    verificador = models.CharField(max_length=100, null=True)
    vehiculo = models.ForeignKey(VerVehiculo, null=True, on_delete=models.PROTECT, related_name='verificaciones_vehiculo_rel')
    conductor = models.ForeignKey(VerConductor, null=True, on_delete=models.PROTECT, related_name='verificaciones_conductor_rel')    
    usuario = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='verificaciones_usuario_rel')

    class Meta:
        db_table = "ver_verificacion"
        ordering = ["-id"]