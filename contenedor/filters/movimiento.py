import django_filters
from contenedor.models import CtnMovimiento

class MovimientoFilter(django_filters.FilterSet):    
    sin_factura = django_filters.BooleanFilter(field_name='factura_id', lookup_expr='isnull', label='Filtrar movimientos sin factura')    
    class Meta:
        model = CtnMovimiento
        fields = {
            'id': ['exact'],
            'tipo': ['exact'],
            'genera_factura': ['exact']
        }