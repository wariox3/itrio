from django.db import models
from general.models.cuenta_banco import GenCuentaBanco

class ConConciliacion(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    cuenta_banco = models.ForeignKey(GenCuentaBanco, null=True, on_delete=models.PROTECT, related_name='conciliaciones_cuenta_banco_rel')

    class Meta:
        db_table = "con_conciliacion"
        ordering = ["-id"]