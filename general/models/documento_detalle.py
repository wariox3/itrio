from django.db import models
from general.models.documento import Documento
from general.models.item import Item
from contabilidad.models.cuenta import Cuenta

class DocumentoDetalle(models.Model):    
    cantidad = models.FloatField(default=0)
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pago = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    base_impuesto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    naturaleza = models.CharField(max_length=1, null=True)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='detalles')
    documento_afectado = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='detalles_afectado', null=True)
    item = models.ForeignKey(Item, null=True, on_delete=models.PROTECT, related_name='itemes')
    cuenta = models.ForeignKey(Cuenta, null=True, on_delete=models.PROTECT, related_name='cuentas')

    class Meta:
        db_table = "gen_documento_detalle"
        ordering = ['id', 'documento', 'item', 'cantidad']