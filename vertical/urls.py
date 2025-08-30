from django.urls import path, include
from .views.entrega import EntregaViewSet
from .views.viaje import ViajeViewSet
from .views.vehiculo import VehiculoViewSet
from .views.conductor import ConductorViewSet
from .views.propuesta import PropuestaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'entrega', EntregaViewSet)
router.register(r'viaje', ViajeViewSet)
router.register(r'vehiculo', VehiculoViewSet)
router.register(r'conductor', ConductorViewSet)
router.register(r'propuesta', PropuestaViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]