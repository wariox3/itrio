from django.db import models
from general.models.documento import Documento
from general.models.cuenta_banco import CuentaBanco

class DocumentoPago(models.Model):    
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentos_pagos_documento')    
    cuenta_banco = models.ForeignKey(CuentaBanco, on_delete=models.PROTECT, related_name='documentos_pagos_cuenta_banco')
    class Meta:
        db_table = "gen_documento_pago"