from django.urls import path, include
from .views.empresa import EmpresaViewSet
from .views.plan import PlanViewSet
from .views.consumo import ConsumoViewSet
from .views.usuario_empresa import UsuarioEmpresaViewSet
from .views.verificacion import VerificacionViewSet
from .views.movimiento import MovimientoViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'empresa', EmpresaViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'consumo', ConsumoViewSet)
router.register(r'usuarioempresa', UsuarioEmpresaViewSet)
router.register(r'verificacion', VerificacionViewSet)
router.register(r'movimiento', MovimientoViewSet)

urlpatterns = [    
    path('', include(router.urls))
]