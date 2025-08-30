from django.db import models

class VerServicio(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)    
    
    class Meta:
        db_table = "ver_servicio"
        ordering = ["-id"]