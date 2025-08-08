from django.urls import path, include
from .views.negocio import NegocioViewSet
from .views.guia import GuiaViewSet
from .views.vehiculo import VehiculoViewSet
from .views.conductor import ConductorViewSet
from .views.color import ColorViewSet
from .views.marca import MarcaViewSet
from .views.linea import LineaViewSet
from .views.combustible import CombustibleViewSet
from .views.carroceria import CarroceriaViewSet
from .views.configuracion import ConfiguracionViewSet
from .views.operacion import OperacionViewSet
from .views.servicio import ServicioViewSet
from .views.producto import ProductoViewSet
from .views.empaque import EmpaqueViewSet
from .views.ruta import RutaViewSet
from .views.zona import ZonaViewSet
from .views.despacho import DespachoViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'negocio', NegocioViewSet)
router.register(r'guia', GuiaViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'conductor', ConductorViewSet)
router.register(r'color', ColorViewSet)
router.register(r'marca', MarcaViewSet)
router.register(r'linea', LineaViewSet)
router.register(r'combustible', CombustibleViewSet)
router.register(r'carroceria', CarroceriaViewSet)
router.register(r'vehiculo_configuracion', ConfiguracionViewSet)
router.register(r'operacion', OperacionViewSet)
router.register(r'servicio', ServicioViewSet)
router.register(r'producto', ProductoViewSet)
router.register(r'empaque', EmpaqueViewSet)
router.register(r'ruta', RutaViewSet)
router.register(r'zona', ZonaViewSet)
router.register(r'despacho', DespachoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]
