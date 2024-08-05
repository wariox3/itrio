from django.urls import path, include
from .views.almacen import InvAlmacenViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'almacen', InvAlmacenViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]