import django_filters
from humano.models.contrato import HumContrato

class ContratoFilter(django_filters.FilterSet):
    #contacto_numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    class Meta:
        model = HumContrato        
        fields = {
            'id': ['exact', 'lte'],
        }