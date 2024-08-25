from django.db import models
from humano.models.concepto import HumConcepto

class HumNovedadTipo(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    nombre = models.CharField(max_length=50)
    novedad_clase_id = models.IntegerField(null=True)
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, null=True, related_name='novedades_tipos_concepto_rel')

    class Meta:
        db_table = "hum_novedad_tipo"