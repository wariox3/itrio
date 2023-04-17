from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contactos', views.ContactoViewSet)
router.register(r'items', views.ItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
]