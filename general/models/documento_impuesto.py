from django.db import models
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.impuesto import GenImpuesto

class GenDocumentoImpuesto(models.Model):   
    base = models.DecimalField(max_digits=20, decimal_places=6, default=0)     
    porcentaje = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    porcentaje_base = models.DecimalField(max_digits=20, decimal_places=6, default=100)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    documento_detalle = models.ForeignKey(GenDocumentoDetalle, on_delete=models.CASCADE)
    impuesto = models.ForeignKey(GenImpuesto, on_delete=models.PROTECT)

    class Meta:
        db_table = "gen_documento_impuesto"