from django.db import models
from humano.models.concepto import HumConcepto
from humano.models.tipo_costo import HumTipoCosto
from contabilidad.models.cuenta import ConCuenta

class HumConceptoCuenta(models.Model):            
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, related_name='conceptos_cuentas_concepto_rel')
    tipo_costo = models.ForeignKey(HumTipoCosto, on_delete=models.PROTECT, related_name='conceptos_cuentas_tipo_costo_rel')
    cuenta = models.ForeignKey(ConCuenta, on_delete=models.PROTECT, related_name='conceptos_cuentas_cuenta_rel')

    class Meta:
        db_table = "hum_concepto_cuenta"
        ordering = ["-id"]