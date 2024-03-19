from django.db import models
from general.models.estado import Estado

class Ciudad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    latitud = models.DecimalField(max_digits=9, decimal_places=9, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=9, null=True)
    codigo_postal = models.CharField(max_length=10, null=True)
    porcentaje_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0)  
    codigo = models.CharField(max_length=10, null=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "gen_ciudad"