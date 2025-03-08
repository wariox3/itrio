from django.db import models
from general.models.documento import GenDocumento
from general.models.item import GenItem
from general.models.contacto import GenContacto
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.grupo import ConGrupo
from humano.models.concepto import HumConcepto
from humano.models.credito import HumCredito
from humano.models.novedad import HumNovedad
from humano.models.contrato import HumContrato
from inventario.models.almacen import InvAlmacen

class GenDocumentoDetalle(models.Model):    
    tipo_registro = models.CharField(max_length=1, default="I") # I=Item, C=Cuenta
    cantidad = models.FloatField(default=0)
    cantidad_operada = models.FloatField(default=0)
    precio = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago_operado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    descuento = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total_bruto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_impuesto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    impuesto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    impuesto_retencion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    impuesto_operado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    hora = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    dias = models.BigIntegerField(default=0)
    base_cotizacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_prestacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_prestacion_vacacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    porcentaje = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    devengado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    deduccion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    naturaleza = models.CharField(max_length=1, null=True)
    operacion = models.BigIntegerField(default=0)
    operacion_inventario = models.BigIntegerField(default=0)
    detalle = models.CharField(max_length=150, null=True)
    numero = models.IntegerField(null=True)
    documento = models.ForeignKey(GenDocumento, on_delete=models.PROTECT, related_name='detalles')
    documento_afectado = models.ForeignKey(GenDocumento, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_documento_afectado_rel')
    item = models.ForeignKey(GenItem, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_item_rel')
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_cuenta_rel')
    grupo = models.ForeignKey(ConGrupo, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_grupo_rel')
    contacto = models.ForeignKey(GenContacto, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_contacto_rel')
    concepto = models.ForeignKey(HumConcepto, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_concepto_rel')
    credito = models.ForeignKey(HumCredito, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_credito_rel')
    novedad = models.ForeignKey(HumNovedad, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_novedad_rel')
    contrato = models.ForeignKey(HumContrato, null=True, on_delete=models.PROTECT,related_name='documentos_detalles_contrato_rel')   
    almacen = models.ForeignKey(InvAlmacen, null=True, on_delete=models.PROTECT, related_name='documentos_detalles_almacen_rel')

    class Meta:
        db_table = "gen_documento_detalle"
        ordering = ['id', 'documento', 'item', 'cantidad']