from django.db import models
from general.models.documento_clase import DocumentoClase
from general.models.resolucion import Resolucion

class DocumentoTipo(models.Model):    
    nombre = models.CharField(max_length=100)
    consecutivo = models.IntegerField(default=1)
    documento_clase = models.ForeignKey(DocumentoClase, null=True, on_delete=models.CASCADE, related_name='documentos_tipos')
    resolucion = models.ForeignKey(Resolucion, null=True, on_delete=models.CASCADE, related_name='documentos_tipos')
    
    class Meta:
        db_table = "gen_documento_tipo"