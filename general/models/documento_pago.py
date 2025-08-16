from django.db import models
from general.models.documento import GenDocumento
from general.models.cuenta_banco import GenCuentaBanco

class GenDocumentoPago(models.Model):    
    pago = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_anulado = models.BooleanField(default = False)
    documento = models.ForeignKey(GenDocumento, on_delete=models.PROTECT, related_name='documentos_pagos_documento')    
    cuenta_banco = models.ForeignKey(GenCuentaBanco, on_delete=models.PROTECT, related_name='documentos_pagos_cuenta_banco')
    class Meta:
        db_table = "gen_documento_pago"
        ordering = ["-id"]