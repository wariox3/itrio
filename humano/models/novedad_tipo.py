from django.db import models
from humano.models.contrato import HumContrato

class HumNovedadTipo(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    nombre = models.CharField(max_length=50)
    novedad_clase_id = models.IntegerField(null=True)

    class Meta:
        db_table = "hum_novedad_tipo"