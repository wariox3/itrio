from django.db import models

class MovimientoDetalle(models.Model):    
    cantidad = models.DecimalField()
    
    class Meta:
        db_table = "gen_movimiento_detalle"