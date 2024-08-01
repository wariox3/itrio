from django.db import models
from general.models.estado import GenEstado

class GenMetodoPago(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    
    class Meta:
        db_table = "gen_metodo_pago"