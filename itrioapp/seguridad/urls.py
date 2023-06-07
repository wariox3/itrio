from django.urls import path, include
from rest_framework import routers
from .views.usuario import UsuarioViewSet, ClaveCambiar, UsuarioEmpresa
from .views.usuario_empresa import UsuarioEmpresaViewSet
from .views.verificacion import VerificacionNuevo, VerificacionToken

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuario")
router.register(r'usuarioempresa', UsuarioEmpresaViewSet, basename="usuario_empresa")

urlpatterns = [
    path('', include(router.urls)),      
    path('verificacion/nuevo/', VerificacionNuevo.as_view(), name = 'verificacion_nuevo'),
    path('verificacion/token/', VerificacionToken.as_view(), name = 'verificacion_token'),
    path('clave/cambiar/', ClaveCambiar.as_view(), name = 'clave_cambiar'),
    path('usuario/empresa/<str:usuario_id>/', UsuarioEmpresa.as_view(), name = 'usuario_empresa'),
]