from django.db import models
from humano.models.aporte import HumAporte
from humano.models.entidad import HumEntidad

class HumAporteEntidad(models.Model):        
    tipo = models.CharField(max_length=20)
    cotizacion = models.DecimalField(max_digits=20, decimal_places=6, default=0) 
    aporte = models.ForeignKey(HumAporte, on_delete=models.PROTECT, related_name='aportes_entidades_aporte_rel')   
    entidad = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, related_name='aportes_entidades_entidad_rel')

    class Meta:
        db_table = "hum_aporte_entidad"