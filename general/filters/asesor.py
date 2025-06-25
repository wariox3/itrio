import django_filters
from general.models.asesor import GenAsesor

class AsesorFilter(django_filters.FilterSet):    
    class Meta:
        model = GenAsesor        
        fields = {
            'id': ['exact', 'lte'],
            'nombre_corto':['icontains']
        }