from django.db import models

class ConComprobante(models.Model):        
    nombre = models.CharField(max_length=100)
    
    class Meta:
        db_table = "con_comprobante"