from django.db import models
from humano.models.programacion import HumProgramacion
from humano.models.contrato import HumContrato

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
    pago_horas = models.BooleanField(default = True)
    pago_auxilio_transporte = models.BooleanField(default = True)
    pago_incapacidad = models.BooleanField(default = True)
    pago_licencia = models.BooleanField(default = True)    
    pago_vacacion = models.BooleanField(default = True)
    descuento_salud = models.BooleanField(default = True)
    descuento_pension = models.BooleanField(default = True)
    descuento_fondo_solidaridad = models.BooleanField(default = True)
    descuento_retencion_fuente = models.BooleanField(default = True)
    descuento_adicional_permanente = models.BooleanField(default = True)
    descuento_adicional_programacion = models.BooleanField(default = True)
    descuento_credito = models.BooleanField(default = True)
    descuento_embargo = models.BooleanField(default = True)
    programacion = models.ForeignKey(HumProgramacion, on_delete=models.PROTECT, related_name='pogramaciones_detalles_programacion_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, related_name='pogramaciones_detalles_contrato_rel')

    class Meta:
        db_table = "hum_programacion_detalle"