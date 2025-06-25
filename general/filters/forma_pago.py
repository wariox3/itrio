import django_filters
from general.models.forma_pago import GenFormaPago

class FormaPagoFilter(django_filters.FilterSet):    
    class Meta:
        model = GenFormaPago        
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}