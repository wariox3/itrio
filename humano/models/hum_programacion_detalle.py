from django.db import models
from humano.models.hum_programacion import HumProgramacion
from humano.models.hum_contrato import HumContrato

class HumProgramacionDetalle(models.Model):            
    diurna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    nocturna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    festiva_diurna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    festiva_nocturna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    extra_diurna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    extra_nocturna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    extra_festiva_diurna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    extra_festiva_nocturna = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    recargo_nocturno = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    recargo_festivo_diurno = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    recargo_festivo_nocturno = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    programacion = models.ForeignKey(HumProgramacion, on_delete=models.PROTECT, related_name='pogramaciones_detalles_programacion_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='pogramaciones_detalles_contrato_rel')

    class Meta:
        db_table = "hum_programacion_detalle"