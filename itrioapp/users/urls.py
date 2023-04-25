from django.urls import path, include
from rest_framework import routers
from users.views import UsuarioViewSet, VerificacionViewSet

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuarios")
router.register('verificacion', VerificacionViewSet, basename="verificaciones")

urlpatterns = [
    path('', include(router.urls)),      
    #path('verificar/', Verificar.as_view(), name = 'verificar'),
]