from django.db import models
from general.models.item import GenItem
from inventario.models.almacen import InvAlmacen

class InvExistencia(models.Model): 
    item = models.ForeignKey(GenItem, on_delete=models.PROTECT, related_name='existencias_item_rel')           
    almacen = models.ForeignKey(InvAlmacen, on_delete=models.PROTECT, related_name='existencias_almacen_rel')
    existencia = models.FloatField(default=0)
    remision = models.FloatField(default=0)
    disponible = models.FloatField(default=0) 

    class Meta:
        db_table = "inv_existencia"
        ordering = ["-id"]