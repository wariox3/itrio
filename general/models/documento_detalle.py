from django.db import models
from general.models.documento import Documento
from general.models.item import Item

class DocumentoDetalle(models.Model):    
    cantidad = models.FloatField(default=0)
    precio = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    total_bruto = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='detalles')
    documento_afectado = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='detalles_afectado', null=True)
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "gen_documento_detalle"
        ordering = ['id', 'documento', 'item', 'cantidad']