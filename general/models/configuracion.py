from django.db import models
from general.models.empresa import GenEmpresa

class GenConfiguracion(models.Model):   
    id = models.BigIntegerField(primary_key=True)     
    formato_factura = models.CharField(max_length=2, default='F')
    informacion_factura = models.TextField(null=True)
    informacion_factura_superior = models.TextField(null=True)
    venta_asesor = models.BooleanField(default = False)
    venta_sede = models.BooleanField(default = False)
    gen_uvt = models.DecimalField(max_digits=20, decimal_places=6, default=47065)
    hum_factor = models.DecimalField(max_digits=6, decimal_places=3, default=7.667)
    hum_salario_minimo = models.DecimalField(max_digits=20, decimal_places=6, default=1300000)
    hum_auxilio_transporte = models.DecimalField(max_digits=20, decimal_places=6, default=162000)
    empresa = models.ForeignKey(GenEmpresa, on_delete=models.PROTECT, default=1)    
    class Meta:
        db_table = "gen_configuracion"