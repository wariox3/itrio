import django_filters
from humano.models.liquidacion import HumLiquidacion

class LiquidacionFilter(django_filters.FilterSet):
    #contacto_numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    class Meta:
        model = HumLiquidacion        
        fields = {
            'id': ['exact', 'lte'],
        }