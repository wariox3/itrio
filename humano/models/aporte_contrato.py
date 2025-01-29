from django.db import models
from humano.models.aporte import HumAporte
from humano.models.contrato import HumContrato
from general.models.ciudad import GenCiudad

class HumAporteContrato(models.Model):        
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    dias = models.IntegerField(default=0)
    salario = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_cotizacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    ingreso = models.BooleanField(default = False)
    retiro = models.BooleanField(default = False)
    error_terminacion = models.BooleanField(default = False)
    aporte = models.ForeignKey(HumAporte, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_aporte_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_contrato_rel')
    ciudad_labora = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_ciudad_labora_rel')

    class Meta:
        db_table = "hum_aporte_contrato"