import django_filters
from contenedor.models import CtnMovimiento

class MovimientoFilter(django_filters.FilterSet):    
    class Meta:
        model = CtnMovimiento
        fields = {
            'id': ['exact'],
            'tipo': ['exact'],
            'documento_fisico': ['exact']
        }