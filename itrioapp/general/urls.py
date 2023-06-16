from django.urls import path, include
from .views.prueba import PruebaView
from .views.item import ItemViewSet
from .views.item_impuesto import ItemImpuestoViewSet
from .views.contacto import ContactoViewSet
from .views.movimiento import MovimientoViewSet
from .views.identificacion import IdentificacionViewSet
from .views.ciudad import CiudadViewSet
from .views.tipo_persona import TipoPersonaViewSet
from .views.regimen import RegimenViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'ciudad', CiudadViewSet)
router.register(r'regimen', RegimenViewSet)
router.register(r'tipopersona', TipoPersonaViewSet)
router.register(r'identificacion', IdentificacionViewSet)
router.register(r'contacto', ContactoViewSet)
router.register(r'item', ItemViewSet)
router.register(r'itemimpuesto', ItemImpuestoViewSet)
router.register(r'movimiento', MovimientoViewSet)


urlpatterns = [    
    path('', include(router.urls)),
    path('prueba/', PruebaView.as_view(), name='prueba')
]