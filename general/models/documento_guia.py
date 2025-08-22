from django.db import models
from general.models.documento import GenDocumento
from transporte.models.guia import TteGuia

class GenDocumentoGuia(models.Model):        
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)    
    documento = models.ForeignKey(GenDocumento, on_delete=models.PROTECT, related_name='documentos_guias_documento_rel')
    guia = models.ForeignKey(TteGuia, on_delete=models.PROTECT, related_name='documentos_guias_guia_rel')

    class Meta:
        db_table = "gen_documento_guia"
        ordering = ['-id']