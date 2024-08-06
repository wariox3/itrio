from django.urls import path, include
from .views.contenedor import ContenedorViewSet
from .views.plan import PlanViewSet
from .views.consumo import ConsumoViewSet
from .views.usuario_contenedor import UsuarioContenedorViewSet
from .views.verificacion import VerificacionViewSet
from .views.movimiento import MovimientoViewSet
from .views.informacion_facturacion import InformacionFacturacionViewSet
from .views.general import ListaAutocompletarView
from .views.session import CtnSessionView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'contenedor', ContenedorViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'consumo', ConsumoViewSet)
router.register(r'usuariocontenedor', UsuarioContenedorViewSet)
router.register(r'verificacion', VerificacionViewSet)
router.register(r'movimiento', MovimientoViewSet)
router.register(r'informacion_facturacion', InformacionFacturacionViewSet)

urlpatterns = [    
    path('', include(router.urls)),
    path('session/lista/', CtnSessionView.as_view(), name='session'),
    path('funcionalidad/lista-autocompletar/', ListaAutocompletarView.as_view(), name='contenedor'),
]