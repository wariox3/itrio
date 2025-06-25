import django_filters
from humano.models.novedad import HumNovedad

class NovedadFilter(django_filters.FilterSet):
    class Meta:
        model = HumNovedad        
        fields = {
            'id': ['exact', 'lte'],
        }