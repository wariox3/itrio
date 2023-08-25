from django.urls import path, include
from .views.prueba import PruebaView, enviar_coreo
from .views.general import ListaAdministradorView, ListaAutocompletarView, ListaDocumentoView
from .views.item import ItemViewSet
from .views.impuesto import ImpuestoViewSet
from .views.item_impuesto import ItemImpuestoViewSet
from .views.contacto import ContactoViewSet
from .views.documento import DocumentoViewSet
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
router.register(r'impuesto', ImpuestoViewSet)
router.register(r'itemimpuesto', ItemImpuestoViewSet)
router.register(r'documento', DocumentoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
    path('funcionalidad/lista-administrador/', ListaAdministradorView.as_view(), name='general'),
    path('funcionalidad/lista-documento/', ListaDocumentoView.as_view(), name='general'),
    path('funcionalidad/lista-autocompletar/', ListaAutocompletarView.as_view(), name='general'),
    path('prueba/', PruebaView.as_view(), name='prueba'),
    path('prueba/enviar-correo/', enviar_coreo, name='prueba-enviar-correo')
]