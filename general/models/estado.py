from django.db import models
from general.models.pais import Pais

class Estado(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)

    class Meta:
        db_table = "gen_estado"