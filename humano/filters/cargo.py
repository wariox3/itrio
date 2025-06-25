import django_filters
from humano.models.cargo import HumCargo

class CargoFilter(django_filters.FilterSet):
    class Meta:
        model = HumCargo        
        fields = {
            'id': ['exact', 'lte'],
        }