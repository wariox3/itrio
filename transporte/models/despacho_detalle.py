from django.db import models
from transporte.models.guia import TteGuia
from transporte.models.despacho import TteDespacho

class TteDespachoDetalle(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)        
    unidades = models.FloatField(default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    peso_facturado = models.FloatField(default=0)
    costo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    declara = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    recaudo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cobro_entrega = models.DecimalField(max_digits=20, decimal_places=6, default=0)    
    despacho = models.ForeignKey(TteDespacho, on_delete=models.PROTECT, related_name='despachos_detalles_despacho_rel')    
    guia = models.ForeignKey(TteGuia, on_delete=models.PROTECT, related_name='despachos_detalles_guia_rel')    

    class Meta:
        db_table = "tte_despacho_detalle"
        ordering = ["-id"]