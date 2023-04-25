from django.urls import path, include
from rest_framework import routers
from users.views import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename="usuarios")


urlpatterns = [
    path('', include(router.urls)),  
]