from django.db import models
from humano.models.contrato import HumContrato
from humano.models.concepto import HumConcepto

class HumCredito(models.Model):        
    fecha_inicio = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cuota = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    abono = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    saldo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cantidad_cuotas = models.IntegerField(default=0)
    cuota_actual = models.IntegerField(default=0)
    validar_cuotas = models.BooleanField(default = True)
    inactivo = models.BooleanField(default = False)    
    inactivo_periodo = models.BooleanField(default = False)
    pagado = models.BooleanField(default = False)
    aplica_prima = models.BooleanField(default = False)    
    aplica_cesantia = models.BooleanField(default = False)
    comentario = models.CharField(max_length=300, null=True)
    concepto = models.ForeignKey(HumConcepto, on_delete=models.PROTECT, null=True, related_name='creditos_concepto_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='creditos_contrato_rel')

    class Meta:
        db_table = "hum_credito"