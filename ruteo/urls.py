from django.urls import path, include
from .views.rut_guia import RutGuiaViewSet
from .views.rut_vehiculo import RutVehiculoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'guia', RutGuiaViewSet)
router.register(r'vehiculo', RutVehiculoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]