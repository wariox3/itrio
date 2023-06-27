from django.urls import path, include
from .views.empresa import EmpresaViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'empresa', EmpresaViewSet)

urlpatterns = [    
    path('', include(router.urls))
]