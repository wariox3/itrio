from django.urls import path, include
from general.views import ContactoViewSet, ItemViewSet, PruebaView
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contactos', ContactoViewSet)
router.register(r'items', ItemViewSet)


urlpatterns = [    
    path('', include(router.urls)),
    path('prueba/', PruebaView.as_view(), name='prueba'),
    path('vista/', views.vista, name='vista'),
    path('vistatemplate/', views.vistaTamplate, name='vistatemplate'),
]