from django.db import models
from general.models.movimiento import Movimiento
from general.models.item import Item

class MovimientoDetalle(models.Model):    
    cantidad = models.FloatField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name='detalles')
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "gen_movimiento_detalle"