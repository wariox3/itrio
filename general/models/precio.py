from django.db import models

class GenPrecio(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=1)
    fecha_vence = models.DateField()
    
    class Meta:
        db_table = "gen_precio"  
        ordering = ["-id"]