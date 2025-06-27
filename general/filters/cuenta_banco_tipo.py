import django_filters
from general.models.cuenta_banco_tipo import GenCuentaBancoTipo

class CuentaBancoTipoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenCuentaBancoTipo        
        fields = {
            'id': ['exact', 'lte'],
            'nombre':['icontains']
        }