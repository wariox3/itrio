from django.db import models
from general.models.documento_clase import GenDocumentoClase
from general.models.resolucion import GenResolucion
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.comprobante import ConComprobante

class GenDocumentoTipo(models.Model):    
    nombre = models.CharField(max_length=100)
    consecutivo = models.IntegerField(default=1)
    venta = models.BooleanField(default = False)
    compra = models.BooleanField(default = False)
    cobrar = models.BooleanField(default = False)
    pagar = models.BooleanField(default = False)
    electronico = models.BooleanField(default = False)
    contabilidad = models.BooleanField(default = False)
    operacion = models.IntegerField(default=0)
    documento_clase = models.ForeignKey(GenDocumentoClase, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_documento_clase')
    resolucion = models.ForeignKey(GenResolucion, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_resolucion')
    cuenta_cobrar = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_cuenta_cobrar')
    cuenta_pagar = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_cuenta_pagar')
    comprobante = models.ForeignKey(ConComprobante, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_comprobante_rel')
    
    class Meta:
        db_table = "gen_documento_tipo"