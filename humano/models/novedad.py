from django.db import models
from humano.models.contrato import HumContrato
from humano.models.novedad_tipo import HumNovedadTipo

class HumNovedad(models.Model):   
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()     
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='novedades_contrato_rel')
    novedad_tipo = models.ForeignKey(HumNovedadTipo, on_delete=models.PROTECT, null=True, related_name='novedades_novedad_tipo_rel')

    class Meta:
        db_table = "hum_novedad"