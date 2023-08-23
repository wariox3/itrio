from django.db import models

class DocumentoClase(models.Model):    
    nombre = models.CharField(max_length=100)
        
    class Meta:
        db_table = "gen_documento_clase"