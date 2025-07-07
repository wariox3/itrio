import django_filters
from contabilidad.models.movimiento import ConMovimiento

class MovimientoFilter(django_filters.FilterSet):    
    class Meta:
        model = ConMovimiento
        fields = {'id': ['exact'],
                  'documento_id': ['exact']}