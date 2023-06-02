from django.urls import path, include
from rest_framework import routers
from users.views import UsuarioViewSet, VerificacionNuevo, VerificacionToken, ClaveCambiar

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path('', include(router.urls)),      
    path('verificacion/nuevo/', VerificacionNuevo.as_view(), name = 'verificacion_nuevo'),
    path('verificacion/token/', VerificacionToken.as_view(), name = 'verificacion_token'),
    path('clave/cambiar/', ClaveCambiar.as_view(), name = 'clave_cambiar'),
]