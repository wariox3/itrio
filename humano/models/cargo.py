from django.db import models

class HumCargo(models.Model):  
    id = models.BigIntegerField(primary_key=True) 
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    estado_inactivo = models.BooleanField(default = False) 

    class Meta:
        db_table = "hum_cargo"