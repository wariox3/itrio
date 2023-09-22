from django.db import models

class Resolucion(models.Model):        
    prefijo = models.CharField(max_length=50)
    numero = models.CharField(max_length=50)
    consecutivo_desde = models.IntegerField()
    consecutivo_hasta = models.IntegerField()
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()

    class Meta:
        db_table = "gen_resolucion"