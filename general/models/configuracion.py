from django.db import models
from general.models.empresa import GenEmpresa
from general.models.documento_tipo import GenDocumentoTipo
from humano.models.entidad import HumEntidad

class GenConfiguracion(models.Model):   
    id = models.BigIntegerField(primary_key=True)         
    informacion_factura = models.TextField(null=True)
    informacion_factura_superior = models.TextField(null=True)
    gen_uvt = models.DecimalField(max_digits=20, decimal_places=6, default=49799)
    gen_emitir_automaticamente = models.BooleanField(default = False)
    hum_factor = models.DecimalField(max_digits=6, decimal_places=3, default=7.666)
    hum_salario_minimo = models.DecimalField(max_digits=20, decimal_places=6, default=1423500)
    hum_auxilio_transporte = models.DecimalField(max_digits=20, decimal_places=6, default=200000)
    empresa = models.ForeignKey(GenEmpresa, on_delete=models.PROTECT, default=1)    
    hum_entidad_riesgo = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True)  
    pos_documento_tipo = models.ForeignKey(GenDocumentoTipo, on_delete=models.PROTECT, null=True)  
    rut_sincronizar_complemento = models.BooleanField(default = False)    
    rut_rutear_franja = models.BooleanField(default = False)
    rut_direccion_origen = models.TextField(null=True)
    rut_latitud = models.DecimalField(max_digits=25, decimal_places=15, null=True)
    rut_longitud = models.DecimalField(max_digits=25, decimal_places=15, null=True)
    class Meta:
        db_table = "gen_configuracion"
        ordering = ["-id"]