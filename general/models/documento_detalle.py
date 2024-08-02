from django.db import models
from general.models.documento import GenDocumento
from general.models.item import GenItem
from general.models.contacto import GenContacto
from contabilidad.models.cuenta import ConCuenta
from decimal import Decimal, ROUND_HALF_UP

class GenDocumentoDetalle(models.Model):    
    cantidad = models.FloatField(default=0)
    precio = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    descuento = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total_bruto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_impuesto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    impuesto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    naturaleza = models.CharField(max_length=1, null=True)
    detalle = models.CharField(max_length=150, null=True)
    numero = models.IntegerField(null=True)
    documento = models.ForeignKey(GenDocumento, on_delete=models.PROTECT, related_name='detalles')
    documento_afectado = models.ForeignKey(GenDocumento, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_documento_afectado_rel')
    item = models.ForeignKey(GenItem, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_item_rel')
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_cuenta_rel')
    contacto = models.ForeignKey(GenContacto, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_contacto_rel')
    class Meta:
        db_table = "gen_documento_detalle"
        ordering = ['id', 'documento', 'item', 'cantidad']