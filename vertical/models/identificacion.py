from django.db import models
from general.models.pais import GenPais
from general.models.tipo_persona import GenTipoPersona

class VerIdentificacion(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10, null=True)
    codigo = models.CharField(max_length=10, null=True)
    
    class Meta:
        db_table = "ver_identificacion"