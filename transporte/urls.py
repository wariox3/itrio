from django.urls import path, include
from .views.guia import GuiaViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'guia', GuiaViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]