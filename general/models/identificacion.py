from django.db import models
from general.models.pais import GenPais
from general.models.tipo_persona import GenTipoPersona

class GenIdentificacion(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10, null=True)    
    orden = models.BigIntegerField(default=0)
    codigo = models.CharField(max_length=10, null=True)
    aporte = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(GenPais, on_delete=models.PROTECT, null=True)
    tipo_persona = models.ForeignKey(GenTipoPersona, on_delete=models.PROTECT, null=True)
    
    class Meta:
        db_table = "gen_identificacion"