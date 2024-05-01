from django.db import models
from general.models.precio import Precio
from general.models.item import Item

class PrecioDetalle(models.Model):    
    vr_precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio = models.ForeignKey(Precio, on_delete=models.PROTECT, related_name='detalles')
    item = models.ForeignKey(Item, null=True, on_delete=models.PROTECT)

    class Meta:
        db_table = "gen_precio_detalle"
        ordering = ['id']