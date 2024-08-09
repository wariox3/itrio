from django.db import models

class ConPeriodo(models.Model):        
    id = models.BigIntegerField(primary_key=True) 
    anio = models.BigIntegerField()
    mes = models.BigIntegerField()
    
    class Meta:
        db_table = "con_periodo"