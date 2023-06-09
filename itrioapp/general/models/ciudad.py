from django.db import models
from general.models.estado import Estado

class Ciudad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)   
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "gen_ciudad"