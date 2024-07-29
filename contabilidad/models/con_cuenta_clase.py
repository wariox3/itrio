from django.db import models

class ConCuentaClase(models.Model):    
    id = models.IntegerField(primary_key=True)    
    nombre = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "con_cuenta_clase"