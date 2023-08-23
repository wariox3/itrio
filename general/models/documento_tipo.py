from django.db import models
from general.models.documento_clase import DocumentoClase

class DocumentoTipo(models.Model):    
    nombre = models.CharField(max_length=100)
    documento_clase = models.ForeignKey(DocumentoClase, null=True, on_delete=models.CASCADE, related_name='documentos_tipos')
    
    class Meta:
        db_table = "gen_documento_tipo"