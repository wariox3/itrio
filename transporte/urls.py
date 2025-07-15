from django.urls import path, include
from .views.guia import GuiaViewSet
from .views.vehiculo import VehiculoViewSet
from .views.conductor import ConductorViewSet
from .views.color import ColorViewSet
from .views.marca import MarcaViewSet
from .views.linea import LineaViewSet
from .views.combustible import CombustibleViewSet
from .views.carroceria import CarroceriaViewSet
from .views.configuracion import ConfiguracionViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'guia', GuiaViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'conductor', ConductorViewSet)
router.register(r'color', ColorViewSet)
router.register(r'marca', MarcaViewSet)
router.register(r'linea', LineaViewSet)
router.register(r'combustible', CombustibleViewSet)
router.register(r'carroceria', CarroceriaViewSet)
router.register(r'vehiculo_configuracion', ConfiguracionViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]