from django.urls import path, include
from .views.hum_contrato import HumMovimientoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contrato', HumMovimientoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]