from django.db import models

class HumConcepto(models.Model):        
    nombre = models.CharField(max_length=80)  
    porcentaje = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    ingreso_base_prestacion = models.BooleanField(default = False)
    ingreso_base_cotizacion = models.BooleanField(default = False)
    orden = models.IntegerField(default = 0)


    class Meta:
        db_table = "hum_concepto"