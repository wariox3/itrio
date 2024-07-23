from django.db import models
from humano.models.hum_pago_tipo import HumPagoTipo
from humano.models.hum_grupo import HumGrupo

class HumProgramacion(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    fecha_hasta_periodo = models.DateField()
    nombre = models.CharField(max_length=100, null=True)
    dias = models.IntegerField(default=0)
    contratos = models.IntegerField(default=0)
    neto = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_aprobado = models.BooleanField(default = False)
    grupo = models.ForeignKey(HumGrupo, on_delete=models.PROTECT, related_name='pogramaciones_grupo_rel')
    pago_tipo = models.ForeignKey(HumPagoTipo, on_delete=models.PROTECT, related_name='pogramaciones_pago_tipo_rel')

    class Meta:
        db_table = "hum_programacion"