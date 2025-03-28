from django.urls import path, include
from .views.visita import RutVisitaViewSet
from .views.vehiculo import RutVehiculoViewSet
from .views.franja import RutFranjaViewSet
from .views.despacho import RutDespachoViewSet
from .views.flota import RutFlotaViewSet
from .views.ubicacion import RutUbicacionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'visita', RutVisitaViewSet)
router.register(r'vehiculo', RutVehiculoViewSet)
router.register(r'franja', RutFranjaViewSet)
router.register(r'despacho', RutDespachoViewSet)
router.register(r'flota', RutFlotaViewSet)
router.register(r'ubicacion', RutUbicacionViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]