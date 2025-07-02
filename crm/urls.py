from django.urls import path, include
from .views.presupuesto import PresupuestoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'presupuesto', PresupuestoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]