import django_filters
from contabilidad.models.grupo import ConGrupo

class GrupoFilter(django_filters.FilterSet):    
    class Meta:
        model = ConGrupo
        fields = {'id': ['exact']}