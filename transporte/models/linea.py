from django.db import models
from transporte.models.marca import TteMarca

class TteLinea(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10) 
    marca = models.ForeignKey(TteMarca, null=True, on_delete=models.PROTECT, related_name='lineas_marca_rel')
    
    class Meta:
        db_table = "tte_linea"
        ordering = ["-id"]