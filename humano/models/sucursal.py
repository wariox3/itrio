from django.db import models

class HumSucursal(models.Model):        
    nombre = models.CharField(max_length=80)  

    class Meta:
        db_table = "hum_sucursal"