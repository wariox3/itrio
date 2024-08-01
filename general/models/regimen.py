from django.db import models

class GenRegimen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    codigo_interface = models.CharField(max_length=2, null=True)
    
    class Meta:
        db_table = "gen_regimen"