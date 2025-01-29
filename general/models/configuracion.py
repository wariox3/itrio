from django.db import models
from general.models.empresa import GenEmpresa
from humano.models.entidad import HumEntidad

class GenConfiguracion(models.Model):   
    id = models.BigIntegerField(primary_key=True)         
    informacion_factura = models.TextField(null=True)
    informacion_factura_superior = models.TextField(null=True)
    venta_asesor = models.BooleanField(default = False)
    venta_sede = models.BooleanField(default = False)
    gen_uvt = models.DecimalField(max_digits=20, decimal_places=6, default=49799)
    hum_factor = models.DecimalField(max_digits=6, decimal_places=3, default=7.666)
    hum_salario_minimo = models.DecimalField(max_digits=20, decimal_places=6, default=1423500)
    hum_auxilio_transporte = models.DecimalField(max_digits=20, decimal_places=6, default=200000)
    empresa = models.ForeignKey(GenEmpresa, on_delete=models.PROTECT, default=1)    
    hum_entidad_riesgo = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True)    
    class Meta:
        db_table = "gen_configuracion"