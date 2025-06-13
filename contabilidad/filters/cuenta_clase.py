import django_filters
from contabilidad.models.cuenta_clase import ConCuentaClase

class CuentaClaseFilter(django_filters.FilterSet):    
    class Meta:
        model = ConCuentaClase
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}