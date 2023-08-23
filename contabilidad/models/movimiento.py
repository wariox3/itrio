from django.db import models
from contabilidad.models.cuenta import Cuenta
from general.models.contacto import Contacto
from general.models.documento import Documento

class Movimiento(models.Model):    
    numero = models.IntegerField(null=True)
    fecha = models.DateField(null=True)
    debito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cuenta = models.ForeignKey(Cuenta, null=True, on_delete=models.CASCADE, related_name='con_movimientos')
    contacto = models.ForeignKey(Contacto, null=True, on_delete=models.CASCADE, related_name='con_movimientos')
    documento = models.ForeignKey(Documento, null=True, on_delete=models.CASCADE, related_name='con_movimientos')

    class Meta:
        db_table = "con_movimiento"