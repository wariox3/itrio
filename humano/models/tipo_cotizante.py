from django.db import models

class HumTipoCotizante(models.Model):  
    id = models.BigIntegerField(primary_key=True)   
    codigo = models.CharField(max_length=20)   
    nombre = models.CharField(max_length=200)    

    class Meta:
        db_table = "hum_tipo_cotizante"
        ordering = ["-id"]