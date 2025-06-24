from django.db import models
from general.models.item import GenItem
from general.models.impuesto import GenImpuesto

class GenItemImpuesto(models.Model):
    item = models.ForeignKey(GenItem, on_delete=models.CASCADE, related_name='itemImpuestos')
    impuesto = models.ForeignKey(GenImpuesto, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('item', 'impuesto')
        db_table = "gen_item_impuesto"
        ordering = ["-id"]
