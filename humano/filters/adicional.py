import django_filters
from humano.models.adicional import HumAdicional

class AdicionalFilter(django_filters.FilterSet):
    class Meta:
        model = HumAdicional        
        fields = {
            'id': ['exact', 'lte'],
        }