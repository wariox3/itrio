from django.db import models
from general.models.documento_detalle import DocumentoDetalle
from general.models.impuesto import Impuesto

class DocumentoImpuesto(models.Model):   
    base = models.DecimalField(max_digits=15, decimal_places=3, default=0)     
    porcentaje = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    porcentaje_base = models.DecimalField(max_digits=15, decimal_places=3, default=100)
    total = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    documento_detalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.PROTECT)

    class Meta:
        db_table = "gen_documento_impuesto"