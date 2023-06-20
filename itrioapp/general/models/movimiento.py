from django.db import models
from general.models.movimiento_clase import MovimientoClase
from general.models.movimiento_tipo import MovimientoTipo
class Movimiento(models.Model):    
    fecha = models.DateField()
    movimiento_tipo = models.ForeignKey(MovimientoTipo, null=True, on_delete=models.CASCADE, related_name='movimientos')

    class Meta:
        db_table = "gen_movimiento"