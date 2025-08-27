from django.db import models

class VerMarca(models.Model):        
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10) 
    remolque = models.BooleanField(default = False)

    class Meta:
        db_table = "ver_marca"
        ordering = ["-id"]