import django_filters
from contabilidad.models.movimiento import ConMovimiento

class MovimientoFilter(django_filters.FilterSet):   
    cuenta__codigo = django_filters.CharFilter(field_name='cuenta__codigo', lookup_expr='icontains') 
    class Meta:
        model = ConMovimiento
        fields = {'id': ['exact'],
                  'documento_id': ['exact'],
                  'cuenta__codigo': ['icontains'],
                  'fecha': ['gte', 'lte'],}