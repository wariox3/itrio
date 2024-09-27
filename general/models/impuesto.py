from django.db import models
from general.models.impuesto_tipo import GenImpuestoTipo

class GenImpuesto(models.Model):
    nombre = models.CharField(max_length=20)
    nombre_extendido = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    porcentaje_base = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    operacion = models.IntegerField(default=1)
    venta = models.BooleanField()
    compra = models.BooleanField()
    impuesto_tipo = models.ForeignKey(GenImpuestoTipo, null=True, on_delete=models.PROTECT, related_name='impuestos_impuesto_tipo_rel')

    class Meta:
        db_table = "gen_impuesto"