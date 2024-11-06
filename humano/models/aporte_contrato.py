from django.db import models
from humano.models.aporte import HumAporte
from humano.models.contrato import HumContrato

class HumAporteContrato(models.Model):        
    dias = models.IntegerField(default=0)
    salario = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_cotizacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    aporte = models.ForeignKey(HumAporte, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_aporte_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_contrato_rel')

    class Meta:
        db_table = "hum_aporte_contrato"