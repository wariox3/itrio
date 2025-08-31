from django.db import models
from vertical.models.viaje import VerViaje
from seguridad.models import User

class VerPropuesta(models.Model):            
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    precio = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    contenedor_id = models.IntegerField(null=True)
    estado_aceptado = models.BooleanField(default = False)
    empresa = models.CharField(max_length=200, null=True)
    viaje = models.ForeignKey(VerViaje, on_delete=models.PROTECT, related_name='propuestas_viaje_rel')    
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='propuestas_usuario_rel')

    class Meta:
        db_table = "ver_propuesta"
        ordering = ["-id"]