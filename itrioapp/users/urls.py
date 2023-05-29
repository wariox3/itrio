from django.urls import path, include
from rest_framework import routers
from users.views import UsuarioViewSet, VerificacionNuevo, VerificacionToken

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path('', include(router.urls)),      
    path('verificacion/nuevo/', VerificacionNuevo.as_view(), name = 'verificacion'),
    path('verificacion/token/', VerificacionToken.as_view(), name = 'verificacion'),
]