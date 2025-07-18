from django.urls import path, include
from .views.contrato import HumContratoViewSet
from .views.grupo import HumGrupoViewSet
from .views.programacion import HumProgramacionViewSet
from .views.programacion_detalle import HumProgramacionDetalleViewSet
from .views.concepto_tipo import HumConceptoTipoViewSet
from .views.concepto import HumConceptoViewSet
from .views.adicional import HumAdicionalViewSet
from .views.novedad_tipo import HumNovedadTipoViewSet
from .views.novedad import HumNovedadViewSet
from .views.credito import HumCreditoViewSet
from .views.sucursal import HumSucursalViewSet
from .views.riesgo import HumRiesgoViewSet
from .views.cargo import HumCargoViewSet
from .views.tipo_cotizante import HumTipoCotizanteViewSet
from .views.subtipo_cotizante import HumSubtipoCotizanteViewSet
from .views.contrato_tipo import HumContratoTipoViewSet
from .views.salud import HumSaludViewSet
from .views.pension import HumPensionViewSet
from .views.concepto_nomina import HumConceptoNominaViewSet
from .views.periodo import HumPeriodoViewSet
from .views.entidad import HumEntidadViewSet
from .views.aporte import HumAporteViewSet
from .views.aporte_contrato import HumAporteContratoViewSet
from .views.aporte_detalle import HumAporteDetalleViewSet
from .views.aporte_entidad import HumAporteEntidadViewSet
from .views.concepto_cuenta import HumConceptoCuentaViewSet
from .views.configuracion_provision import HumConfiguracionProvisionViewSet
from .views.configuracion_aporte import HumConfiguracionAporteViewSet
from .views.liquidacion import HumLiquidacionViewSet
from .views.motivo_terminacion import HumMotivoTerminacionViewSet
from .views.tiempo import HumTiempoViewSet
from .views.tipo_costo import HumTipoCostoViewSet
from .views.pago_tipo import HumPagoTipoViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contrato', HumContratoViewSet)
router.register(r'contrato_tipo', HumContratoTipoViewSet)
router.register(r'grupo', HumGrupoViewSet)
router.register(r'concepto_tipo', HumConceptoTipoViewSet)
router.register(r'concepto', HumConceptoViewSet)
router.register(r'adicional', HumAdicionalViewSet)
router.register(r'novedad_tipo', HumNovedadTipoViewSet)
router.register(r'novedad', HumNovedadViewSet)
router.register(r'credito', HumCreditoViewSet)
router.register(r'programacion', HumProgramacionViewSet)
router.register(r'programacion_detalle', HumProgramacionDetalleViewSet)
router.register(r'sucursal', HumSucursalViewSet)
router.register(r'riesgo', HumRiesgoViewSet)
router.register(r'cargo', HumCargoViewSet)
router.register(r'tipo_cotizante', HumTipoCotizanteViewSet)
router.register(r'subtipo_cotizante', HumSubtipoCotizanteViewSet)
router.register(r'salud', HumSaludViewSet)
router.register(r'pension', HumPensionViewSet)
router.register(r'concepto_nomina', HumConceptoNominaViewSet)
router.register(r'periodo', HumPeriodoViewSet)
router.register(r'entidad', HumEntidadViewSet)
router.register(r'aporte', HumAporteViewSet)
router.register(r'aporte_contrato', HumAporteContratoViewSet)
router.register(r'aporte_detalle', HumAporteDetalleViewSet)
router.register(r'aporte_entidad', HumAporteEntidadViewSet)
router.register(r'concepto_cuenta', HumConceptoCuentaViewSet)
router.register(r'configuracion_provision', HumConfiguracionProvisionViewSet)
router.register(r'configuracion_aporte', HumConfiguracionAporteViewSet)
router.register(r'liquidacion', HumLiquidacionViewSet)
router.register(r'motivo_terminacion', HumMotivoTerminacionViewSet)
router.register(r'tiempo', HumTiempoViewSet)
router.register(r'tipo_costo', HumTipoCostoViewSet)
router.register(r'pago_tipo', HumPagoTipoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]