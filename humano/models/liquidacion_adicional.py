from django.db import models
from humano.models.liquidacion import HumLiquidacion
from humano.models.contrato import HumContrato
from rest_framework import serializers

class HumLiquidacionAdicional(models.Model):        
    adicional = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    deduccion = models.DecimalField(max_digits=20, decimal_places=6, default=0)    
    liquidacion = models.ForeignKey(HumLiquidacion, on_delete=models.PROTECT, related_name='liquidaciones_adicionales_liquidacion_rel')

    class Meta:
        db_table = "hum_liquidacion_adicional"
        ordering = ["-id"]