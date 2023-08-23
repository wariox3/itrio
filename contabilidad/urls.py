from django.urls import path, include
from .views.movimiento import MovimientoViewSet
from .views.cuenta import CuentaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'movimiento', MovimientoViewSet)
router.register(r'cuenta', CuentaViewSet)


urlpatterns = [    
    path('', include(router.urls)),
]