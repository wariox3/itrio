import django_filters
from humano.models.periodo import HumPeriodo

class PeriodoFilter(django_filters.FilterSet):
    class Meta:
        model = HumPeriodo        
        fields = {
            'id': ['exact', 'lte'],
        }