from django.db import models

class CuentaBancoTipo(models.Model):
    nombre = models.CharField(max_length=100)
    
    class Meta:
        db_table = "gen_cuenta_banco_tipo"  