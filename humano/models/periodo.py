from django.db import models

class HumPeriodo(models.Model):  
    id = models.BigIntegerField(primary_key=True) 
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200) 
    dias = models.IntegerField(default=0)

    class Meta:
        db_table = "hum_periodo"
        ordering = ["-id"]