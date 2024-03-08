from django.db import models

class Item(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    codigo = models.CharField(max_length=100, null=True, verbose_name='Codigo')
    referencia = models.CharField(max_length=50, null=True, verbose_name='Referencia')
    costo = models.FloatField(default=0, verbose_name='Costo')
    precio = models.FloatField(default=0, verbose_name='Precio')

    class Meta:
        db_table = "gen_item"  