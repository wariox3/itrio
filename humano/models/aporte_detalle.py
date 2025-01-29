from django.db import models
from humano.models.aporte_contrato import HumAporteContrato

class HumAporteDetalle(models.Model):     
    ingreso = models.BooleanField(default = False)
    retiro = models.BooleanField(default = False)
    variacion_permanente_salario = models.BooleanField(default = False)
    variacion_transitoria_salario = models.BooleanField(default = False)
    suspension_temporal_contrato = models.BooleanField(default = False)
    
    aporte_contrato = models.ForeignKey(HumAporteContrato, on_delete=models.PROTECT, related_name='aportes_detalles_aporte_contrato_rel')

    class Meta:
        db_table = "hum_aporte_detalle"