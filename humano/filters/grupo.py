import django_filters
from humano.models.grupo import HumGrupo

class GrupoFilter(django_filters.FilterSet):
    class Meta:
        model = HumGrupo        
        fields = {
            'id': ['exact', 'lte'],
        }