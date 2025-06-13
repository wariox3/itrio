import django_filters
from contabilidad.models.cuenta import ConCuenta

class CuentaFilter(django_filters.FilterSet):    
    class Meta:
        model = ConCuenta
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains'],
                  'codigo': ['exact','icontains']}