import django_filters
from humano.models.credito import HumCredito

class CreditoFilter(django_filters.FilterSet):
    class Meta:
        model = HumCredito        
        fields = {
            'id': ['exact', 'lte'],
        }