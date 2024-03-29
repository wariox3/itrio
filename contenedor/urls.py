from django.urls import path, include
from .views.contenedor import ContenedorViewSet
from .views.plan import PlanViewSet
from .views.consumo import ConsumoViewSet
from .views.usuario_contenedor import UsuarioContenedorViewSet
from .views.verificacion import VerificacionViewSet
from .views.movimiento import MovimientoViewSet
from .views.general import ListaAutocompletarView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'contenedor', ContenedorViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'consumo', ConsumoViewSet)
router.register(r'usuariocontenedor', UsuarioContenedorViewSet)
router.register(r'verificacion', VerificacionViewSet)
router.register(r'movimiento', MovimientoViewSet)

urlpatterns = [    
    path('', include(router.urls)),
    path('funcionalidad/lista-autocompletar/', ListaAutocompletarView.as_view(), name='contenedor'),
]