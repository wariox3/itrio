from django.db import models
from general.models.pais import Pais

class Departamento(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    #Relaciones    
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)


    class Meta:
        db_table = "gen_departamento"