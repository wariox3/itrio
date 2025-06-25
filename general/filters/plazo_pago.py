import django_filters
from general.models.plazo_pago import GenPlazoPago

class PlazoPagoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenPlazoPago        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }