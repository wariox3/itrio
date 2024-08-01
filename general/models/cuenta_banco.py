from django.db import models
from general.models.cuenta_banco_tipo import GenCuentaBancoTipo

class GenCuentaBanco(models.Model):
    nombre = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50, null=True)
    cuenta_banco_tipo = models.ForeignKey(GenCuentaBancoTipo, on_delete=models.PROTECT, related_name='cuentas_bancos')
    
    class Meta:
        db_table = "gen_cuenta_banco"  