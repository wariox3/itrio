from django.db import models
from general.models.item import Item
from general.models.impuesto import Impuesto

class ItemImpuesto(models.Model):
    nombre = models.CharField(max_length=200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemImpuestos')
    impuesto = models.ForeignKey(Impuesto, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('item', 'impuesto')
        db_table = "gen_item_impuesto"
