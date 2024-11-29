from django.db import models
from contabilidad.models.cuenta_clase import ConCuentaClase
from contabilidad.models.cuenta_grupo import ConCuentaGrupo
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta
from contabilidad.models.cuenta_subcuenta import ConCuentaSubcuenta

class ConCuenta(models.Model):        
    codigo = models.CharField(max_length=20, default="0", unique=True)
    nombre = models.CharField(max_length=100)
    exige_base = models.BooleanField(default = False)
    exige_tercero = models.BooleanField(default = False)
    exige_grupo = models.BooleanField(default = False)
    permite_movimiento = models.BooleanField(default = False)
    nivel = models.IntegerField(null=True) 
    cuenta_clase = models.ForeignKey(ConCuentaClase, on_delete=models.PROTECT, null=True)
    cuenta_grupo = models.ForeignKey(ConCuentaGrupo, on_delete=models.PROTECT, null=True)
    cuenta_cuenta = models.ForeignKey(ConCuentaCuenta, on_delete=models.PROTECT, null=True)
    cuenta_subcuenta = models.ForeignKey(ConCuentaSubcuenta, on_delete=models.PROTECT, null=True)
    
    class Meta:
        db_table = "con_cuenta"