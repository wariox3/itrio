from django.db import models
from humano.models.pago_tipo import HumPagoTipo
from humano.models.grupo import HumGrupo

class HumProgramacion(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    fecha_hasta_periodo = models.DateField()
    nombre = models.CharField(max_length=100, null=True)
    dias = models.IntegerField(default=0)
    contratos = models.IntegerField(default=0)
    neto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_aprobado = models.BooleanField(default = False)
    estado_generado = models.BooleanField(default = False)
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
    comentario = models.CharField(max_length=300, null=True)
    grupo = models.ForeignKey(HumGrupo, on_delete=models.PROTECT, related_name='pogramaciones_grupo_rel')
    pago_tipo = models.ForeignKey(HumPagoTipo, on_delete=models.PROTECT, related_name='pogramaciones_pago_tipo_rel')

    class Meta:
        db_table = "hum_programacion"