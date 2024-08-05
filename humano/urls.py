from django.urls import path, include
from .views.contrato import HumMovimientoViewSet
from .views.grupo import HumGrupoViewSet
from .views.programacion import HumProgramacionViewSet
from .views.programacion_detalle import HumProgramacionDetalleViewSet
from .views.concepto import HumConceptoViewSet
from .views.adicional import HumAdicionalViewSet
from .views.novedad import HumNovedadViewSet
from .views.credito import HumCreditoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contrato', HumMovimientoViewSet)
router.register(r'grupo', HumGrupoViewSet)
router.register(r'concepto', HumConceptoViewSet)
router.register(r'adicional', HumAdicionalViewSet)
router.register(r'novedad', HumNovedadViewSet)
router.register(r'credito', HumCreditoViewSet)
router.register(r'programacion', HumProgramacionViewSet)
router.register(r'programacion_detalle', HumProgramacionDetalleViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]