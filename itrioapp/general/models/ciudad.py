from django.db import models
from general.models.departamento import Departamento

class Ciudad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    #Relaciones    
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "gen_ciudad"