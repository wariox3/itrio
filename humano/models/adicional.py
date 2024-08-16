from django.db import models
from humano.models.contrato import HumContrato
from humano.models.concepto import HumConcepto
from humano.models.programacion import HumProgramacion

class HumAdicional(models.Model):        
    valor = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    horas = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    aplica_dia_laborado = models.BooleanField(default = False)
    inactivo = models.BooleanField(default = False)
    inactivo_periodo = models.BooleanField(default = False)
    permanente = models.BooleanField(default = False)
    detalle = models.CharField(max_length=200, null=True)
    programacion = models.ForeignKey(HumProgramacion, on_delete=models.PROTECT, null=True, related_name='adicionales_programacion_rel')
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, related_name='adicionales_concepto_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='adicionales_contrato_rel')

    class Meta:
        db_table = "hum_adicional"