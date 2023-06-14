from django.db import models

class Item(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=100, null=True)
    referencia = models.CharField(max_length=50, null=True)
    costo = models.FloatField(default=0)
    precio = models.FloatField(default=0)

    class Meta:
        db_table = "gen_item"  