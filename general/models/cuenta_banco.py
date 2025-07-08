from django.db import models
from general.models.cuenta_banco_tipo import GenCuentaBancoTipo
from general.models.cuenta_banco_clase import GenCuentaBancoClase
from contabilidad.models.cuenta import ConCuenta

class GenCuentaBanco(models.Model):
    nombre = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50, null=True)
    cuenta_banco_tipo = models.ForeignKey(GenCuentaBancoTipo, on_delete=models.PROTECT, related_name='cuentas_bancos_cuenta_banco_tipo')
    cuenta_banco_clase = models.ForeignKey(GenCuentaBancoClase, null=True, on_delete=models.PROTECT, related_name='cuentas_bancos_cuenta_banco_clase')
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='cuentas_bancos_cuenta_rel')

    class Meta:
        db_table = "gen_cuenta_banco"  
        ordering = ["nombre"]