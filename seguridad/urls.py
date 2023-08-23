from django.urls import path, include
from rest_framework import routers
from .views.usuario import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename="usuario")

urlpatterns = [
    path('', include(router.urls))
]