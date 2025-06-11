from django.db import models

class ConPeriodo(models.Model):        
    id = models.BigIntegerField(primary_key=True) 
    anio = models.BigIntegerField()
    mes = models.BigIntegerField()
    estado_bloqueado = models.BooleanField(default = False)
    estado_cerrado = models.BooleanField(default = False)
    estado_inconsistencia = models.BooleanField(default = False)

    class Meta:
        db_table = "con_periodo"
        ordering = ["-id"]