from django.db import models

class HumPagoTipo(models.Model):  
    id = models.BigIntegerField(primary_key=True)      
    nombre = models.CharField(max_length=100)    
    aplica_programacion = models.BooleanField(default = False)    

    class Meta:
        db_table = "hum_pago_tipo"