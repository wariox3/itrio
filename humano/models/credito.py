from django.db import models
from humano.models.contrato import HumContrato

class HumCredito(models.Model):        
    fecha_inicio = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cuota = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cantidad_cuotas = models.IntegerField(default=0)
    validar_cuotas = models.BooleanField(default = True)
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='creditos_contrato_rel')
    class Meta:
        db_table = "hum_credito"