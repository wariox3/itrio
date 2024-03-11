from django.db import models
from general.models.pais import Pais

class Identificacion(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10, null=True)    
    orden = models.BigIntegerField(default=0)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "gen_identificacion"