from django.db import models
from general.models.documento import GenDocumento
from transporte.models.guia import TteGuia

class GenDocumentoGuia(models.Model):        
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)        
    unidades = models.FloatField(default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    peso_facturado = models.FloatField(default=0)
    costo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    declara = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    recaudo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cobro_entrega = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    documento = models.ForeignKey(GenDocumento, on_delete=models.PROTECT, related_name='documentos_guias_documento_rel')
    guia = models.ForeignKey(TteGuia, on_delete=models.PROTECT, related_name='documentos_guias_guia_rel')

    class Meta:
        db_table = "gen_documento_guia"
        ordering = ['-id']