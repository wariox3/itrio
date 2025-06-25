import django_filters
from general.models.cuenta_banco_clase import GenCuentaBancoClase

class CuentaBancoClaseFilter(django_filters.FilterSet):    
    class Meta:
        model = GenCuentaBancoClase        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }