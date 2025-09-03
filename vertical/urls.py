from django.urls import path, include
from .views.entrega import EntregaViewSet
from .views.viaje import ViajeViewSet
from .views.vehiculo import VehiculoViewSet
from .views.conductor import ConductorViewSet
from .views.propuesta import PropuestaViewSet
from .views.empaque import EmpaqueViewSet
from .views.servicio import ServicioViewSet
from .views.producto import ProductoViewSet
from .views.ciudad import CiudadViewSet
from .views.precio_detalle import PrecioDetalleViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'entrega', EntregaViewSet)
router.register(r'viaje', ViajeViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'conductor', ConductorViewSet)
router.register(r'propuesta', PropuestaViewSet)
router.register(r'empaque', EmpaqueViewSet)
router.register(r'servicio', ServicioViewSet)
router.register(r'producto', ProductoViewSet)
router.register(r'ciudad', CiudadViewSet)
router.register(r'precio_detalle', PrecioDetalleViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]