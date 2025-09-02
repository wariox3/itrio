import django_filters
from humano.models.contrato import HumContrato

class ContratoFilter(django_filters.FilterSet):
    contacto__numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    contacto__nombre_corto = django_filters.CharFilter(field_name='contacto__nombre_corto', lookup_expr='icontains')
    class Meta:
        model = HumContrato        
        fields = {
            'id': ['exact', 'lte'],
            'estado_terminado':['exact'],
            'contacto__numero_identificacion': ['exact', 'icontains'],
            'contacto__nombre_corto': ['exact','icontains'],
        }