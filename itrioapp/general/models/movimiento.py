from django.db import models

class Movimiento(models.Model):    
    fecha = models.DateField()
    
    class Meta:
        db_table = "gen_movimiento"