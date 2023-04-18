from django.urls import path, include
from . import views
from rest_framework import routers
from inquilino.views import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename="usuarios")


urlpatterns = [
    path('', include(router.urls)),
]