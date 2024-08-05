from django.db import models
from general.models.documento import GenDocumento

class GenErrorImportar(models.Model):    
    fila = models.IntegerField(default=0)
    mensaje = models.CharField(max_length=150, null=True)    
    documento = models.ForeignKey(GenDocumento, on_delete=models.CASCADE, related_name='errores_importar_documento_rel')
    
    class Meta:
        db_table = "gen_error_importar"