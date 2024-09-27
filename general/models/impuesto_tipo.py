from django.db import models

class GenImpuestoTipo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=20)

    class Meta:
        db_table = "gen_impuesto_tipo"