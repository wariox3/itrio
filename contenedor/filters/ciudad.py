import django_filters
from contenedor.models import CtnCiudad

class CiudadFilter(django_filters.FilterSet):    
    class Meta:
        model = CtnCiudad
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }