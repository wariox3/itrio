import django_filters
from humano.models.novedad import HumNovedad

class NovedadFilter(django_filters.FilterSet):
    novedad_tipo__nombre = django_filters.CharFilter(field_name='novedad_tipo__nombre', lookup_expr='icontains')
    contrato__contacto__numero_identificacion = django_filters.CharFilter(field_name='contrato__contacto__numero_identificacion', lookup_expr='icontains')
    contrato__contacto__nombre_corto = django_filters.CharFilter(field_name='contrato__contacto__nombre_corto', lookup_expr='icontains')
    class Meta:
        model = HumNovedad        
        fields = {
            'id': ['exact', 'lte'],
            'novedad_tipo__nombre': ['exact', 'icontains'],
            'contrato__contacto__numero_identificacion': ['exact', 'icontains'],
            'contrato__contacto__nombre_corto': ['exact', 'icontains'],
            'fecha_desde': ['gte', 'lte', 'gt', 'lt', 'exact'], 
            'fecha_hasta': ['gte', 'lte', 'gt', 'lt', 'exact'], 
        }