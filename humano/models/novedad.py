from django.db import models
from humano.models.contrato import HumContrato

class HumNovedad(models.Model):   
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()     
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='novedades_contrato_rel')


    class Meta:
        db_table = "hum_novedad"