from django.db import models
from general.models.documento import GenDocumento

class GenArchivo(models.Model):    
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=500)    
    tipo = models.CharField(max_length=100)
    tamano = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    almacenamiento_id = models.CharField(max_length=255)
    documento = models.ForeignKey(GenDocumento, null=True, on_delete=models.PROTECT, related_name='archivos_documento_rel')

    class Meta:
        db_table = "gen_archivo"