from django.db import models

class HumConceptoTipo(models.Model):        
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)  
    
    class Meta:
        db_table = "hum_concepto_tipo"
        ordering = ["-id"]