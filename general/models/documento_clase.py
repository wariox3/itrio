from django.db import models

class GenDocumentoClase(models.Model):    
    nombre = models.CharField(max_length=100)
    grupo = models.IntegerField(null=True)
    codigo_dian = models.CharField(max_length=2, default='01')
        
    class Meta:
        db_table = "gen_documento_clase"
        ordering = ["-id"]