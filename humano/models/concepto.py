from django.db import models
from humano.models.concepto_tipo import HumConceptoTipo

class HumConcepto(models.Model):        
    nombre = models.CharField(max_length=80)  
    porcentaje = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    ingreso_base_prestacion = models.BooleanField(default = False)
    ingreso_base_prestacion_vacacion = models.BooleanField(default = False)
    ingreso_base_cotizacion = models.BooleanField(default = False)    
    operacion = models.BigIntegerField(default=0)
    orden = models.IntegerField(default = 0)
    adicional = models.BooleanField(default = False)
    concepto_tipo = models.ForeignKey(HumConceptoTipo, on_delete=models.PROTECT, null=True, related_name='conceptos_concepto_tipo_rel')
    
    class Meta:
        db_table = "hum_concepto"
        ordering = ["id"]