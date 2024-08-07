from django.db import models

class GenImpuesto(models.Model):
    nombre = models.CharField(max_length=20)
    nombre_extendido = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    porcentaje_base = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    venta = models.BooleanField()
    compra = models.BooleanField()

    class Meta:
        db_table = "gen_impuesto"