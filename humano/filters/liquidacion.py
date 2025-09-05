import django_filters
from humano.models.liquidacion import HumLiquidacion

class LiquidacionFilter(django_filters.FilterSet):
    contrato__contacto_numero_identificacion = django_filters.CharFilter(field_name='contrato__contacto__numero_identificacion', lookup_expr='icontains')
    contrato__contacto__nombre_corto = django_filters.CharFilter(field_name='contrato__contacto__nombre_corto', lookup_expr='icontains')
    class Meta:
        model = HumLiquidacion        
        fields = {
            'id': ['exact', 'lte'],
            'contrato__contacto__numero_identificacion': ['exact', 'icontains'],
            'contrato__contacto__nombre_corto': ['exact','icontains'],
        }