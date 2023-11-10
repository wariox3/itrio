from django.db import models

class Resolucion(models.Model):        
    prefijo = models.CharField(max_length=50, null=True)
    numero = models.CharField(max_length=50, null=True)
    clave_tecnica = models.CharField(max_length=500, null=True)
    ambiente = models.CharField(max_length=10, null=True)
    set_prueba = models.CharField(max_length=500, null=True)
    consecutivo_desde = models.IntegerField()
    consecutivo_hasta = models.IntegerField()
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

    class Meta:
        db_table = "gen_resolucion"