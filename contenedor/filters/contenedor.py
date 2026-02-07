import django_filters
from contenedor.models import Contenedor

class ContenedorFilter(django_filters.FilterSet):    
    
    class Meta:
        model = Contenedor
        fields = {
            'id': ['exact'],
        }