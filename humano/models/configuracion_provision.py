from django.db import models
from humano.models.tipo_costo import HumTipoCosto
from contabilidad.models.cuenta import ConCuenta

class HumConfiguracionProvision(models.Model):  
    id = models.BigIntegerField(primary_key=True)   
    tipo = models.CharField(max_length=20, null=True)    
    orden = models.IntegerField(default = 0)
    tipo_costo = models.ForeignKey(HumTipoCosto, on_delete=models.PROTECT, null=True, related_name='configuraciones_provisiones_tipo_costo_rel')
    cuenta_debito = models.ForeignKey(ConCuenta, on_delete=models.PROTECT, null=True, related_name='configuraciones_provisiones_cuenta_debito_rel')
    cuenta_credito = models.ForeignKey(ConCuenta, on_delete=models.PROTECT, null=True, related_name='configuraciones_provisiones_cuenta_credito_rel')

    class Meta:
        db_table = "hum_configuracion_provision"