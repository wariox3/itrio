from django.db import models

class Pais(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    class Meta:
        db_table = "gen_pais"