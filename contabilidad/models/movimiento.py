from django.db import models
from contabilidad.models.cuenta import ConCuenta
from general.models.contacto import GenContacto
from general.models.documento import Documento

class ConMovimiento(models.Model):    
    numero = models.IntegerField(null=True)
    fecha = models.DateField(null=True)
    debito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='movimientos_cuenta_re')
    contacto = models.ForeignKey(GenContacto, null=True, on_delete=models.PROTECT, related_name='movimientos_contacto_rel')
    documento = models.ForeignKey(Documento, null=True, on_delete=models.PROTECT, related_name='movimientos_documento_rel')

    class Meta:
        db_table = "con_movimiento"