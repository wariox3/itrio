from django.db import models
from general.models.cuenta_banco_tipo import CuentaBancoTipo

class CuentaBanco(models.Model):
    nombre = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50, null=True)
    cuenta_banco_tipo = models.ForeignKey(CuentaBancoTipo, on_delete=models.CASCADE, related_name='cuentas_bancos')
    
    class Meta:
        db_table = "gen_cuenta_banco"  