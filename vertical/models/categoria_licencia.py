from django.db import models

class VerCategoriaLicencia(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=2) 
    
    class Meta:
        db_table = "ver_categoria_licencia"
        ordering = ["id"]