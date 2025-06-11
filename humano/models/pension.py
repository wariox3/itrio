from django.db import models
from humano.models.concepto import HumConcepto

class HumPension(models.Model):  
    id = models.BigIntegerField(primary_key=True) 
    nombre = models.CharField(max_length=50) 
    porcentaje_empleado = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    porcentaje_empleador = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, null=True, related_name='pensiones_concepto_rel')

    class Meta:
        db_table = "hum_pension"
        ordering = ["-id"]