import django_filters
from general.models.identificacion import GenIdentificacion

class IdentificacionFilter(django_filters.FilterSet):    
    class Meta:
        model = GenIdentificacion        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }