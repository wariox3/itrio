import django_filters
from general.models.cuenta_banco import GenCuentaBanco

class CuentaBancoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenCuentaBanco
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}