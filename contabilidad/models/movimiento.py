from django.db import models
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.comprobante import ConComprobante
from contabilidad.models.grupo import ConGrupo
from contabilidad.models.periodo import ConPeriodo
from general.models.contacto import GenContacto
from general.models.documento import GenDocumento

class ConMovimiento(models.Model):    
    numero = models.IntegerField(null=True)
    fecha = models.DateField()
    debito = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    credito = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    naturaleza = models.CharField(max_length=1)
    detalle = models.CharField(max_length=150, null=True)
    cierre = models.BooleanField(default = False)
    comprobante = models.ForeignKey(ConComprobante, on_delete=models.PROTECT, related_name='movimientos_comprobante_rel')
    cuenta = models.ForeignKey(ConCuenta, on_delete=models.PROTECT, related_name='movimientos_cuenta_rel')
    grupo = models.ForeignKey(ConGrupo, null=True, on_delete=models.PROTECT, related_name='movimientos_grupo_rel')
    periodo = models.ForeignKey(ConPeriodo, on_delete=models.PROTECT, related_name='movimientos_periodo_rel')
    contacto = models.ForeignKey(GenContacto, null=True, on_delete=models.PROTECT, related_name='movimientos_contacto_rel')
    documento = models.ForeignKey(GenDocumento, null=True, on_delete=models.PROTECT, related_name='movimientos_documento_rel')


    class Meta:
        db_table = "con_movimiento"