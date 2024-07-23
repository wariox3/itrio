from django.urls import path, include
from .views.hum_contrato import HumMovimientoViewSet
from .views.hum_grupo import HumGrupoViewSet
from .views.hum_programacion import HumProgramacionViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contrato', HumMovimientoViewSet)
router.register(r'grupo', HumGrupoViewSet)
router.register(r'programacion', HumProgramacionViewSet)

urlpatterns = [    
    path('', include(router.urls)),
]