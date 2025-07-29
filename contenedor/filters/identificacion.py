import django_filters
from contenedor.models import CtnIdentificacion

class IdentificacionFilter(django_filters.FilterSet):    
    class Meta:
        model = CtnIdentificacion
        fields = {
            'id': ['exact', 'lte']}