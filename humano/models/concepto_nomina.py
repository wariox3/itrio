from django.db import models
from humano.models.concepto import HumConcepto

class HumConceptoNomina(models.Model):  
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)        
    concepto = models.ForeignKey(HumConcepto, null=True, on_delete=models.PROTECT, related_name='conceptos_nomina_concepto_rel')

    class Meta:
        db_table = "hum_concepto_nomina"
        ordering = ['-id']