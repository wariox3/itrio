import django_filters
from contabilidad.models.conciliacion_detalle import ConConciliacionDetalle

class ConciliacionDetalleFilter(django_filters.FilterSet):    
    class Meta:
        model = ConConciliacionDetalle
        fields = {'id': ['exact'],
                'conciliacion_id': ['exact'],
                'estado_conciliado': ['exact']}