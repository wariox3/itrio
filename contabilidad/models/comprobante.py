from django.db import models

class ConComprobante(models.Model): 
    id = models.IntegerField(primary_key=True)       
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, null=True)
    permite_asiento = models.BooleanField(default = False)
    
    class Meta:
        db_table = "con_comprobante"