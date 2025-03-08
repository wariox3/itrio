from django.db import models
from contabilidad.models.cuenta import ConCuenta

class HumConfiguracionAporte(models.Model):  
    id = models.BigIntegerField(primary_key=True)   
    tipo = models.CharField(max_length=20, null=True)    
    orden = models.IntegerField(default = 0)    
    cuenta = models.ForeignKey(ConCuenta, on_delete=models.PROTECT, null=True, related_name='configuraciones_aportes_cuenta_rel')    

    class Meta:
        db_table = "hum_configuracion_aporte"