from django.db import models

class Item(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_general = models.CharField(max_length=100, null=True)
    referencia = models.CharField(max_length=50, null=True)
    costo_predeterminado = models.FloatField(default=0)
    precio_predeterminado = models.FloatField(default=0)
    codigo_impuesto_compra_fkm = models.IntegerField(null=True)
    codigo_impuesto_venta_fkm = models.IntegerField(null=True)
    codigo_cuenta_venta_fk = models.IntegerField(null=True)
    codigo_cuenta_costo_venta_fk = models.IntegerField(null=True)
    codigo_cuenta_inventario_fk = models.IntegerField(null=True)
    codigo_marca_fk = models.IntegerField(null=True)
    codigo_medida_fkm = models.IntegerField(null=True)

    class Meta:
        db_table = "gen_item"  