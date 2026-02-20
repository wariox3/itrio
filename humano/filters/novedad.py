import django_filters
from humano.models.novedad import HumNovedad

class NovedadFilter(django_filters.FilterSet):
    novedad_tipo__nombre = django_filters.CharFilter(field_name='novedad_tipo__nombre', lookup_expr='icontains')
    class Meta:
        model = HumNovedad        
        fields = {
            'id': ['exact', 'lte'],
            'novedad_tipo__nombre': ['exact', 'icontains'],
        }