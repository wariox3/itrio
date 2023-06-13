from django.db import models

class Impuesto(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)
    nombre_extendido = models.CharField(max_length=100)
    porcentaje = models.DecimalField(default=0)
    venta = models.BooleanField()
    compra = models.BooleanField()

    class Meta:
        db_table = "gen_impuesto"