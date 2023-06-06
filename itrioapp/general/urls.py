from django.urls import path, include
from .views.prueba import PruebaView
from .views.item import ItemViewSet
from .views.contacto import ContactoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contacto', ContactoViewSet)
router.register(r'item', ItemViewSet)


urlpatterns = [    
    path('', include(router.urls)),
    path('prueba/', PruebaView.as_view(), name='prueba')
]