from django.db import models
from humano.models.concepto import HumConcepto

class HumSalud(models.Model):  
    id = models.BigIntegerField(primary_key=True) 
    nombre = models.CharField(max_length=50)  
    porcentaje_empleado = models.DecimalField(max_digits=6, decimal_places=3, default=4)
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, null=True, related_name='saludes_concepto_rel')

    class Meta:
        db_table = "hum_salud"
        ordering = ["id"]