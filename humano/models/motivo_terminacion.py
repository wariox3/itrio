from django.db import models

class HumMotivoTerminacion(models.Model):        
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)  
    
    class Meta:
        db_table = "hum_motivo_terminacion"
        ordering = ["-id"]