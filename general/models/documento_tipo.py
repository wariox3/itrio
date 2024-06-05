from django.db import models
from general.models.documento_clase import DocumentoClase
from general.models.resolucion import Resolucion
from contabilidad.models.cuenta import Cuenta

class DocumentoTipo(models.Model):    
    nombre = models.CharField(max_length=100)
    consecutivo = models.IntegerField(default=1)
    documento_clase = models.ForeignKey(DocumentoClase, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_documento_clase')
    resolucion = models.ForeignKey(Resolucion, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_resolucion')
    cuenta_cobrar = models.ForeignKey(Cuenta, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_cuenta_cobrar')
    cuenta_pagar = models.ForeignKey(Cuenta, null=True, on_delete=models.PROTECT, related_name='documentos_tipos_cuenta_pagar')
    
    class Meta:
        db_table = "gen_documento_tipo"