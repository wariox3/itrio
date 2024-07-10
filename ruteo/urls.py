from django.urls import path, include
from .views.rut_visita import RutVisitaViewSet
from .views.rut_vehiculo import RutVehiculoViewSet
from .views.rut_franja import RutFranjaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'visita', RutVisitaViewSet)
router.register(r'vehiculo', RutVehiculoViewSet)
router.register(r'franja', RutFranjaViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]