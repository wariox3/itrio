from django.db import models

class HumTipoCosto(models.Model):  
    id = models.BigIntegerField(primary_key=True)       
    nombre = models.CharField(max_length=200)    

    class Meta:
        db_table = "hum_tipo_costo"
        ordering = ["id"]