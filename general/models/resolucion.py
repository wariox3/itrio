from django.db import models

class GenResolucion(models.Model):        
    prefijo = models.CharField(max_length=50, null=True)
    numero = models.CharField(max_length=50, null=True)
    clave_tecnica = models.CharField(max_length=500, null=True)
    set_prueba = models.CharField(max_length=500, null=True)
    consecutivo_desde = models.IntegerField()
    consecutivo_hasta = models.IntegerField()
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    venta = models.BooleanField(default = False)
    compra = models.BooleanField(default = False)

    class Meta:
        db_table = "gen_resolucion"