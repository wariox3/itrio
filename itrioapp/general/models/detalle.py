from django.db import models
from general.models.movimiento import Movimiento

class Detalle(models.Model):    
    cantidad = models.FloatField()
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name='detalles')

    class Meta:
        db_table = "gen_detalle"