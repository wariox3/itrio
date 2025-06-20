from django.db import models
from humano.models.contrato import HumContrato


class HumLiquidacion(models.Model):   
    fecha = models.DateField()
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    dias = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    cesantia = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    interes = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    prima = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    vacacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    deduccion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    adicion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_aprobado = models.BooleanField(default = False)
    estado_generado = models.BooleanField(default = False)    
    comentario = models.CharField(max_length=300, null=True)
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='liquidaciones_contrato_rel')    

    class Meta:
        db_table = "hum_liquidacion"
        ordering = ["-id"]