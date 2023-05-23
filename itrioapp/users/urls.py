from django.urls import path, include
from rest_framework import routers
from users.views import UsuarioViewSet, VerificacionAPIView

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet, basename="usuarios")

urlpatterns = [
    path('', include(router.urls)),      
    path('verificacion/', VerificacionAPIView.as_view(), name = 'verificacion'),
]