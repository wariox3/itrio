from django.urls import path, include
from .views.parametro import ParametroViewSet
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
from .views.verificacion import VerificacionViewSet
from .views.verificacion_detalle import VerificacionDetalleViewSet
from .views.identificacion import IdentificacionViewSet
from .views.categoria_licencia import CategoriaLicenciaViewSet
from .views.carroceria import CarroceriaViewSet
from .views.color import ColorViewSet
from .views.combustible import CombustibleViewSet
from .views.vehiculo_configuracion import VehiculoConfiguracionViewSet
from .views.linea import LineaViewSet
from .views.marca import MarcaViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'parametro', ParametroViewSet)
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
router.register(r'verificacion', VerificacionViewSet)
router.register(r'verificacion_detalle', VerificacionDetalleViewSet)
router.register(r'identificacion', IdentificacionViewSet)
router.register(r'categoria_licencia', CategoriaLicenciaViewSet)
router.register(r'ciudad', CiudadViewSet)
router.register(r'carroceria', CarroceriaViewSet)
router.register(r'color', ColorViewSet)
router.register(r'combustible', CombustibleViewSet)
router.register(r'vehiculo_configuracion', VehiculoConfiguracionViewSet)
router.register(r'linea', LineaViewSet)
router.register(r'marca', MarcaViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]