from django.db import models

class GenRegimen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)
    codigo_interface = models.CharField(max_length=2, null=True)
    inactivo = models.BooleanField(default = False)
    
    class Meta:
        db_table = "gen_regimen"
        ordering = ["nombre"]