from django.db import models
from general.models.movimiento_detalle import MovimientoDetalle
from general.models.impuesto import Impuesto

class MovimientoImpuesto(models.Model):   
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)     
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    movimiento_detalle = models.ForeignKey(MovimientoDetalle, on_delete=models.CASCADE)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.CASCADE)

    class Meta:
        db_table = "gen_movimiento_impuesto"