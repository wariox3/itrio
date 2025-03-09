from django.db import models
from humano.models.aporte import HumAporte
from humano.models.contrato import HumContrato
from humano.models.entidad import HumEntidad
from humano.models.riesgo import HumRiesgo
from general.models.ciudad import GenCiudad

class HumAporteContrato(models.Model):        
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    dias = models.IntegerField(default=0)
    salario = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    base_cotizacion = models.DecimalField(max_digits=20, decimal_places=6, default=0)     
    cotizacion_pension = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_pension_total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_pension_empresa = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_pension_empleado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_voluntario_pension_afiliado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_voluntario_pension_aportante = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_solidaridad_solidaridad = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_solidaridad_subsistencia = models.DecimalField(max_digits=20, decimal_places=6, default=0)    
    cotizacion_salud = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_salud_empresa = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_salud_empleado = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_riesgos = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_caja = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_sena = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_icbf = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cotizacion_total = models.DecimalField(max_digits=20, decimal_places=6, default=0)        
    ingreso = models.BooleanField(default = False)
    retiro = models.BooleanField(default = False)
    error_terminacion = models.BooleanField(default = False)        
    aporte = models.ForeignKey(HumAporte, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_aporte_rel')
    contrato = models.ForeignKey(HumContrato, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_contrato_rel')
    ciudad_labora = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_ciudad_labora_rel')
    entidad_salud = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_entidad_salud_rel')
    entidad_pension = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_entidad_pension_rel')    
    entidad_caja = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_entidad_caja_rel')
    entidad_riesgo = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_entidad_riesgo_rel')
    entidad_sena = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_entidad_sena_rel')
    entidad_icbf = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_entidad_icbf_rel')
    riesgo = models.ForeignKey(HumRiesgo, on_delete=models.PROTECT, null=True, related_name='aportes_contratos_riesgo_rel')

    class Meta:
        db_table = "hum_aporte_contrato"