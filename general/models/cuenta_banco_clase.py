from django.db import models

class GenCuentaBancoClase(models.Model):
    nombre = models.CharField(max_length=30)
    
    class Meta:
        db_table = "gen_cuenta_banco_clase"  
        ordering = ["nombre"]