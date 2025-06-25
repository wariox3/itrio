import django_filters
from general.models.tipo_persona import GenTipoPersona

class TipoPersonaFilter(django_filters.FilterSet):    
    class Meta:
        model = GenTipoPersona        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }