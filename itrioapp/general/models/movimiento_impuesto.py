from django.db import models
from general.models.movimiento_detalle import MovimientoDetalle
from general.models.impuesto import Impuesto

class MovimientoImpuesto(models.Model):        
    movimiento_detalle = models.ForeignKey(MovimientoDetalle, on_delete=models.CASCADE)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.CASCADE)

    class Meta:
        db_table = "gen_movimiento_impuesto"