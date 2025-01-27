from django.db import models
from humano.models.aporte_contrato import HumAporteContrato

class HumAporteDetalle(models.Model):        
    aporte_contrato = models.ForeignKey(HumAporteContrato, on_delete=models.PROTECT, related_name='aportes_detalles_aporte_contrato_rel')

    class Meta:
        db_table = "hum_aporte_detalle"