from django.db import models
from contabilidad.models.cuenta_clase import ConCuentaClase

class ConCuenta(models.Model):        
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    exige_base = models.BooleanField(default = False)
    exige_tercero = models.BooleanField(default = False)
    exige_grupo = models.BooleanField(default = False)
    permite_movimiento = models.BooleanField(default = False)
    cuenta_clase = models.ForeignKey(ConCuentaClase, on_delete=models.PROTECT, null=True)
    
    class Meta:
        db_table = "con_cuenta"