from django.urls import path, include
from .views.movimiento import MovimientoViewSet
from .views.cuenta import CuentaViewSet
from .views.cuenta_clase import CuentaClaseViewSet
from .views.cuenta_grupo import CuentaGrupoViewSet
from .views.cuenta_cuenta import CuentaCuentaViewSet
from .views.cuenta_subcuenta import CuentaSubcuentaViewSet
from .views.comprobante import ComprobanteViewSet
from .views.grupo import GrupoViewSet
from .views.periodo import PeriodoViewSet
from .views.activo import ActivoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'movimiento', MovimientoViewSet)
router.register(r'cuenta', CuentaViewSet)
router.register(r'cuenta_clase', CuentaClaseViewSet)
router.register(r'cuenta_grupo', CuentaGrupoViewSet)
router.register(r'cuenta_cuenta', CuentaCuentaViewSet)
router.register(r'cuenta_subcuenta', CuentaSubcuentaViewSet)
router.register(r'comprobante', ComprobanteViewSet)
router.register(r'grupo', GrupoViewSet)
router.register(r'periodo', PeriodoViewSet)
router.register(r'activo', ActivoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]