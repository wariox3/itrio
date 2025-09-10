from django.db import models

class VerVerificacionConcepto(models.Model):        
    id = models.BigIntegerField(primary_key=True)
    tipo = models.CharField(max_length=1)
    nombre = models.CharField(max_length=100)
    
    class Meta:
        db_table = "ver_verificacion_concepto"
        ordering = ["-id"]