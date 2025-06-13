import django_filters
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta

class CuentaCuentaFilter(django_filters.FilterSet):    
    class Meta:
        model = ConCuentaCuenta
        fields = {'id': ['exact', 'gte', 'lte'],
                  'nombre': ['exact','icontains']}