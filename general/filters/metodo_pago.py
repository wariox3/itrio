import django_filters
from general.models.metodo_pago import GenMetodoPago

class MetodoPagoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenMetodoPago        
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}