from django.db import models
from humano.models.contrato import HumContrato
from humano.models.novedad_tipo import HumNovedadTipo

class HumNovedad(models.Model):   
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()  
    fecha_desde_periodo = models.DateField(null=True)
    fecha_hasta_periodo = models.DateField(null=True)
    dias_disfrutados = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    dias_disfrutados_reales = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    dias_dinero = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    pago_disfrute = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago_dinero = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pago_dia_disfrute = models.DecimalField(max_digits=20, decimal_places=6, default=0)       
    pago_dia_dinero = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='novedades_contrato_rel')
    novedad_tipo = models.ForeignKey(HumNovedadTipo, on_delete=models.PROTECT, null=True, related_name='novedades_novedad_tipo_rel')

    class Meta:
        db_table = "hum_novedad"