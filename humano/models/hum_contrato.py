from django.db import models

class HumContrato(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

    class Meta:
        db_table = "hum_contrato"