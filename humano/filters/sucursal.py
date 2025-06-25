import django_filters
from humano.models.sucursal import HumSucursal

class SucursalFilter(django_filters.FilterSet):
    class Meta:
        model = HumSucursal        
        fields = {
            'id': ['exact', 'lte'],
        }