import django_filters
from inventario.models.existencia import InvExistencia

class InvExistenciaFilter(django_filters.FilterSet):    
    class Meta:
        model = InvExistencia        
        fields = {'id': ['exact'],}