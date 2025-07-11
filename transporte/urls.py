from django.urls import path, include
from .views.guia import GuiaViewSet
from .views.vehiculo import VehiculoViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'guia', GuiaViewSet)
router.register(r'vehiculo', VehiculoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]