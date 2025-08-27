from django.db import models
from vertical.models.estado import VerEstado

class VerCiudad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    codigo_postal = models.CharField(max_length=10, null=True)
    codigo = models.CharField(max_length=10, null=True)
    estado = models.ForeignKey(VerEstado, on_delete=models.PROTECT)
    
    class Meta:
        db_table = "ver_ciudad"
        ordering = ["nombre"]