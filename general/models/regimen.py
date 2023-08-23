from django.db import models

class Regimen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    
    class Meta:
        db_table = "gen_regimen"