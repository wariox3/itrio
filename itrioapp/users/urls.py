from django.urls import path, include
from rest_framework import routers
from users.views import UsuarioViewSet, VerificacionAPIView, VerificacionTokenAPIView

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path('', include(router.urls)),      
    path('verificacion/', VerificacionAPIView.as_view(), name = 'verificacion'),
    path('verificacion/token', VerificacionTokenAPIView.as_view(), name = 'verificacion'),
]