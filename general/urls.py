from django.urls import path, include
from .views.prueba import PruebaView, enviar_coreo
from .views.general import ListaView, AutocompletarView, BuscarView
from .views.item import ItemViewSet
from .views.resolucion import ResolucionViewSet
from .views.impuesto import ImpuestoViewSet
from .views.item_impuesto import ItemImpuestoViewSet
from .views.contacto import ContactoViewSet
from .views.documento_tipo import DocumentoTipoViewSet
from .views.documento import DocumentoViewSet
from .views.documento_detalle import DocumentoDetalleViewSet
from .views.documento_pago import DocumentoPagoViewSet
from .views.identificacion import IdentificacionViewSet
from .views.ciudad import CiudadViewSet
from .views.tipo_persona import TipoPersonaViewSet
from .views.regimen import RegimenViewSet
from .views.metodo_pago import MetodoPagoViewSet
from .views.precio import PrecioViewSet
from .views.precio_detalle import PrecioDetalleViewSet
from .views.cuenta_banco import CuentaBancoViewSet
from .views.asesor import AsesorViewSet
from .views.sede import SedeViewSet
from .views.plazo_pago import PlazoPagoViewSet
from .views.empresa import EmpresaViewSet
from .views.configuracion import ConfiguracionViewSet
from .views.configuracion_usuario import ConfiguracionUsuarioViewSet
from .views.complemento import ComplementoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'ciudad', CiudadViewSet)
router.register(r'regimen', RegimenViewSet)
router.register(r'tipopersona', TipoPersonaViewSet)
router.register(r'identificacion', IdentificacionViewSet)
router.register(r'contacto', ContactoViewSet)
router.register(r'item', ItemViewSet)
router.register(r'resolucion', ResolucionViewSet)
router.register(r'impuesto', ImpuestoViewSet)
router.register(r'itemimpuesto', ItemImpuestoViewSet)
router.register(r'documento_tipo', DocumentoTipoViewSet)
router.register(r'documento', DocumentoViewSet)
router.register(r'documento_detalle', DocumentoDetalleViewSet)
router.register(r'documento_pago', DocumentoPagoViewSet)
router.register(r'metodopago', MetodoPagoViewSet)
router.register(r'precio', PrecioViewSet)
router.register(r'preciodetalle', PrecioDetalleViewSet)
router.register(r'cuenta_banco', CuentaBancoViewSet)
router.register(r'asesor', AsesorViewSet)
router.register(r'sede', SedeViewSet)
router.register(r'plazopago', PlazoPagoViewSet)
router.register(r'empresa', EmpresaViewSet)
router.register(r'configuracion', ConfiguracionViewSet)
router.register(r'configuracion_usuario', ConfiguracionUsuarioViewSet)
router.register(r'complemento', ComplementoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
    path('funcionalidad/lista/', ListaView.as_view(), name='general'),
    path('funcionalidad/autocompletar/', AutocompletarView.as_view(), name='general'),
    path('funcionalidad/buscar/', BuscarView.as_view(), name='general'),
    path('prueba/', PruebaView.as_view(), name='prueba'),
    path('prueba/enviar-correo/', enviar_coreo, name='prueba-enviar-correo')
]