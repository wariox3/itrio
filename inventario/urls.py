from django.urls import path, include
from .views.almacen import InvAlmacenViewSet
from .views.existencia import InvExistenciaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'almacen', InvAlmacenViewSet)
router.register(r'existencia', InvExistenciaViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]