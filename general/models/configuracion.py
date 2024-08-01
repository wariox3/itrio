from django.db import models
from general.models.empresa import Empresa

class GenConfiguracion(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    formato_factura = models.CharField(max_length=2, default='F')
    informacion_factura = models.TextField(null=True)
    informacion_factura_superior = models.TextField(null=True)
    venta_asesor = models.BooleanField(default = False)
    venta_sede = models.BooleanField(default = False)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, default=1)    
    class Meta:
        db_table = "gen_configuracion"