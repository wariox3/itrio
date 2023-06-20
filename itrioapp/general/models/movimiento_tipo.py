from django.db import models
from general.models.movimiento_clase import MovimientoClase

class MovimientoTipo(models.Model):    
    nombre = models.CharField(max_length=100)
    movimiento_clase = models.ForeignKey(MovimientoClase, null=True, on_delete=models.CASCADE, related_name='movimientos_tipos')
    
    class Meta:
        db_table = "gen_movimiento_tipo"