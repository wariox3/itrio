from django.db import models
from general.models.item import Item
from general.models.impuesto import Impuesto

class ItemImpuesto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='itemImpuestos')
    impuesto = models.ForeignKey(Impuesto, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('item', 'impuesto')
        db_table = "gen_item_impuesto"
