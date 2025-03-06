from django.db import models
from humano.models.concepto import HumConcepto
from contabilidad.models.cuenta import ConCuenta

class HumConceptoCuenta(models.Model):            
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, related_name='conceptos_cuentas_concepto_rel')
    cuenta = models.ForeignKey(ConCuenta, on_delete=models.PROTECT, related_name='conceptos_cuentas_cuenta_rel')

    class Meta:
        db_table = "hum_concepto_cuenta"