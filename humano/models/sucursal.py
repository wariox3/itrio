from django.db import models

class HumSucursal(models.Model):        
    nombre = models.CharField(max_length=80) 
    codigo = models.CharField(max_length=10, null=True) 

    class Meta:
        db_table = "hum_sucursal"