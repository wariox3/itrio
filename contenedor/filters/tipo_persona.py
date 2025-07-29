import django_filters
from contenedor.models import CtnTipoPersona

class TipoPersonaFilter(django_filters.FilterSet):    
    class Meta:
        model = CtnTipoPersona
        fields = {
            'id': ['exact', 'lte']}