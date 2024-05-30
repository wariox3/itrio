from django.db import models
from contabilidad.models.cuenta_clase import CuentaClase

class Cuenta(models.Model):    
    id = models.IntegerField(primary_key=True)
    codigo = models.IntegerField(null=True)
    nombre = models.CharField(max_length=100, null=True)
    cuenta_clase = models.ForeignKey(CuentaClase, on_delete=models.PROTECT, null=True)
    
    class Meta:
        db_table = "con_cuenta"