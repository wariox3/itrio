import django_filters
from contabilidad.models.conciliacion_detalle import ConConciliacionDetalle

class ConciliacionDetalleFilter(django_filters.FilterSet):    
    class Meta:
        model = ConConciliacionDetalle
        fields = {'id': ['exact']}