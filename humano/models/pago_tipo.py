from django.db import models
from contabilidad.models.cuenta import ConCuenta

class HumPagoTipo(models.Model):  
    id = models.BigIntegerField(primary_key=True)      
    nombre = models.CharField(max_length=100)    
    aplica_programacion = models.BooleanField(default = False)
    cuenta = models.ForeignKey(ConCuenta, null=True, on_delete=models.PROTECT, related_name='pagos_tipos_cuenta_rel')

    class Meta:
        db_table = "hum_pago_tipo"