from django.urls import path, include
from .views.inquilino import InquilinoViewSet
from .views.plan import PlanViewSet
from .views.consumo import ConsumoViewSet
from .views.usuario_inquilino import UsuarioInquilinoViewSet
from .views.verificacion import VerificacionViewSet
from .views.movimiento import MovimientoViewSet
from .views.general import ListaAutocompletarView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'inquilino', InquilinoViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'consumo', ConsumoViewSet)
router.register(r'usuarioinquilino', UsuarioInquilinoViewSet)
router.register(r'verificacion', VerificacionViewSet)
router.register(r'movimiento', MovimientoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
    path('funcionalidad/lista-autocompletar/', ListaAutocompletarView.as_view(), name='inquilino'),
]