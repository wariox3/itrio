from django.db import models
from contabilidad.models.cuenta import ConCuenta

class GenFormaPago(models.Model):    
    nombre = models.CharField(max_length=50) 
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='formas_pagos_cuenta_rel')
    
    class Meta:
        db_table = "gen_forma_pago"
        ordering = ["id"]