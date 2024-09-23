from django.db import models

class ConCuentaSubcuenta(models.Model):    
    id = models.IntegerField(primary_key=True)    
    nombre = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "con_cuenta_subcuenta"