from django.urls import path, include
from rest_framework import routers
from .views.usuario import UsuarioViewSet, ClaveCambiar, UsuarioEmpresaAPIView, EmpresaNuevoAPIView
from .views.usuario_empresa import UsuarioEmpresaViewSet
from .views.verificacion import VerificacionViewSet

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuario")
router.register(r'verificacion', VerificacionViewSet)
router.register(r'usuarioempresa', UsuarioEmpresaViewSet, basename="usuario_empresa")

urlpatterns = [
    path('', include(router.urls)),      
    path('clave/cambiar/', ClaveCambiar.as_view(), name = 'clave_cambiar'),
    path('usuario/empresa/<str:usuario_id>/', UsuarioEmpresaAPIView.as_view(), name = 'usuario_empresa'),
    path('empresa/nuevo/', EmpresaNuevoAPIView.as_view(), name = 'empresa_nuevo'),
]