from django.urls import path, include
from rest_framework import routers
from .views.informe import PendienteView

router = routers.DefaultRouter()


urlpatterns = [    
    path('', include(router.urls)),
    path('informe/pendiente/', PendienteView.as_view(), name='cartera'),
]