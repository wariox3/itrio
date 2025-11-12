from django.db import models
from vertical.models.verificacion_concepto import VerVerificacionConcepto
from vertical.models.verificacion import VerVerificacion

class VerVerificacionDetalle(models.Model):
    fecha_verificacion = models.DateTimeField(null=True)        
    verificado = models.BooleanField(default = False)
    verificacion = models.ForeignKey(VerVerificacion, on_delete=models.PROTECT, related_name='verificaciones_detalles_verificacion_rel')
    verificacion_concepto = models.ForeignKey(VerVerificacionConcepto, on_delete=models.PROTECT, related_name='verificaciones_detalles_verificacion_concepto_rel')

    class Meta:
        db_table = "ver_verificacion_detalle"
        ordering = ["-id"]