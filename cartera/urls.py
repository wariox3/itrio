from django.urls import path, include
from rest_framework import routers
from .views.informe import InformeView

router = routers.DefaultRouter()


urlpatterns = [    
    path('', include(router.urls)),
    path('informe/pendiente-corte/', InformeView.as_view(), name='cartera'),
]