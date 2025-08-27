from django.db import models
from vertical.models.pais import VerPais

class VerEstado(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(VerPais, on_delete=models.PROTECT)

    class Meta:
        db_table = "ver_estado"
        ordering = ["-id"]