from django.db import models
from contabilidad.models.conciliacion import ConConciliacion
from contabilidad.models.cuenta import ConCuenta
from general.models.contacto import GenContacto
from general.models.documento import GenDocumento

class ConConciliacionDetalle(models.Model):        
    fecha = models.DateField()
    debito = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    credito = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    detalle = models.CharField(max_length=150, null=True)
    estado_conciliado = models.BooleanField(default = False)    
    conciliacion = models.ForeignKey(ConConciliacion, null=True, on_delete=models.PROTECT, related_name='conciliaciones_detalles_conciliacion_rel')
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='conciliaciones_detalles_cuenta_rel')
    contacto = models.ForeignKey(GenContacto, null=True, on_delete=models.PROTECT, related_name='conciliaciones_detalles_contacto_rel')
    documento = models.ForeignKey(GenDocumento, null=True, on_delete=models.PROTECT, related_name='conciliaciones_detalles_documento_rel')

    class Meta:
        db_table = "con_conciliacion_detalle"
        ordering = ["-id"]