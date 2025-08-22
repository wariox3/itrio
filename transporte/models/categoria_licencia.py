from django.db import models

class TteCategoriaLicencia(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    
    class Meta:
        db_table = "tte_categoria_licencia"
        ordering = ["id"]