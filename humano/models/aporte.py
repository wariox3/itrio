from django.db import models
from humano.models.sucursal import HumSucursal
from humano.models.entidad import HumEntidad

class HumAporte(models.Model):        
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    fecha_hasta_periodo = models.DateField(null=True)
    anio = models.BigIntegerField(default=0)
    anio_salud = models.BigIntegerField(default=0)
    mes = models.BigIntegerField(default=0)
    mes_salud = models.BigIntegerField(default=0)
    presentacion = models.CharField(max_length=1, default='S')
    contratos = models.IntegerField(default=0)
    empleados = models.IntegerField(default=0)
    lineas = models.IntegerField(default=0)
    base_cotizacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    pension = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    fondo_solidaridad = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    fondo_subsistencia = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    salud = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    riesgo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    caja = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    sena = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    icbf = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_aprobado = models.BooleanField(default = False)
    estado_generado = models.BooleanField(default = False)
    comentario = models.CharField(max_length=300, null=True)
    sucursal = models.ForeignKey(HumSucursal, on_delete=models.PROTECT, null=True, related_name='aportes_sucursal_rel')
    entidad_riesgo = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True)    

    class Meta:
        db_table = "hum_aporte"