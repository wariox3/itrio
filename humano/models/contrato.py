from django.db import models
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from contabilidad.models.grupo import ConGrupo
from humano.models.contrato_tipo import HumContratoTipo
from humano.models.grupo import HumGrupo
from humano.models.sucursal import HumSucursal
from humano.models.riesgo import HumRiesgo
from humano.models.cargo import HumCargo
from humano.models.salud import HumSalud
from humano.models.pension import HumPension
from humano.models.tipo_cotizante import HumTipoCotizante
from humano.models.subtipo_cotizante import HumSubtipoCotizante
from humano.models.entidad import HumEntidad
from humano.models.tiempo import HumTiempo
from humano.models.tipo_costo import HumTipoCosto
from humano.models.motivo_terminacion import HumMotivoTerminacion

class HumContrato(models.Model):        
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    salario = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    auxilio_transporte = models.BooleanField(default = False)
    salario_integral = models.BooleanField(default = False)
    estado_terminado = models.BooleanField(default = False)    
    comentario = models.CharField(max_length=300, null=True)
    fecha_ultimo_pago = models.DateField(null=True)
    fecha_ultimo_pago_prima = models.DateField(null=True)
    fecha_ultimo_pago_cesantia = models.DateField(null=True)
    fecha_ultimo_pago_vacacion = models.DateField(null=True)
    contrato_tipo = models.ForeignKey(HumContratoTipo, on_delete=models.PROTECT, related_name='contratos_contrato_tipo_rel')
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='contratos_contacto_rel')
    ciudad_contrato = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, null=True, related_name='contratos_ciudad_contrato_rel')
    ciudad_labora = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, null=True, related_name='contratos_ciudad_labora_rel')
    grupo = models.ForeignKey(HumGrupo, on_delete=models.PROTECT, related_name='contratos_grupo_rel')
    sucursal = models.ForeignKey(HumSucursal, on_delete=models.PROTECT, null=True, related_name='contratos_sucursal_rel')
    riesgo = models.ForeignKey(HumRiesgo, on_delete=models.PROTECT, null=True, related_name='contratos_riesgo_rel')
    tipo_cotizante = models.ForeignKey(HumTipoCotizante, null=True, on_delete=models.PROTECT, related_name='contratos_tipo_cotizante_rel')
    subtipo_cotizante = models.ForeignKey(HumSubtipoCotizante, null=True, on_delete=models.PROTECT, related_name='contratos_subtipo_cotizante_rel')
    cargo = models.ForeignKey(HumCargo, on_delete=models.PROTECT, null=True, related_name='contratos_cargo_rel')
    salud = models.ForeignKey(HumSalud, on_delete=models.PROTECT, null=True, related_name='contratos_salud_rel')
    pension = models.ForeignKey(HumPension, on_delete=models.PROTECT, null=True, related_name='contratos_pension_rel')
    entidad_salud = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='contratos_entidad_salud_rel')
    entidad_pension = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='contratos_entidad_pension_rel')
    entidad_cesantias = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='contratos_entidad_cesantias_rel')
    entidad_caja = models.ForeignKey(HumEntidad, on_delete=models.PROTECT, null=True, related_name='contratos_entidad_caja_rel')
    tiempo = models.ForeignKey(HumTiempo, on_delete=models.PROTECT, null=True, related_name='contratos_tiempo_rel')
    tipo_costo = models.ForeignKey(HumTipoCosto, on_delete=models.PROTECT, null=True, related_name='contratos_tipo_costo_rel')
    grupo_contabilidad = models.ForeignKey(ConGrupo, on_delete=models.PROTECT, null=True, related_name='contratos_grupo_contabilidad_rel')
    motivo_terminacion = models.ForeignKey(HumMotivoTerminacion, null=True, on_delete=models.PROTECT, related_name='contratos_motivo_terminacion_rel')
    
    class Meta:
        db_table = "hum_contrato"  
        ordering = ["-id"] 