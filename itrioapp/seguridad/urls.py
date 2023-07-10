from django.urls import path, include
from rest_framework import routers
from .views.usuario import UsuarioViewSet, CambiarClave
from .views.usuario_empresa import UsuarioEmpresaViewSet
from .views.verificacion import VerificacionViewSet

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuario")
router.register(r'verificacion', VerificacionViewSet)
router.register(r'usuarioempresa', UsuarioEmpresaViewSet, basename="usuario_empresa")

urlpatterns = [
    path('', include(router.urls)),      
    path('cambiar-clave/', CambiarClave.as_view(), name = 'cambiar_clave')
]