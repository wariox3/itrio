from django.urls import path, include
from .views.movimiento import MovimientoViewSet
from .views.cuenta import CuentaViewSet
from .views.cuenta_clase import CuentaClaseViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'movimiento', MovimientoViewSet)
router.register(r'cuenta', CuentaViewSet)
router.register(r'cuenta_clase', CuentaClaseViewSet)



urlpatterns = [    
    path('', include(router.urls)),
]