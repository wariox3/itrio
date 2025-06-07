from django.db import models

class TteCarroceria(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10) 
    
    class Meta:
        db_table = "tte_carroceria"