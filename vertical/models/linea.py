from django.db import models
from vertical.models.marca import VerMarca

class VerLinea(models.Model):    
    id = models.BigIntegerField(primary_key=True)    
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10) 
    marca = models.ForeignKey(VerMarca, null=True, on_delete=models.PROTECT, related_name='lineas_marca_rel')

    class Meta:
        db_table = "ver_linea"
        ordering = ["-id"]