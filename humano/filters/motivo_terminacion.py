import django_filters
from humano.models.motivo_terminacion import HumMotivoTerminacion

class MotivoTerminacionFilter(django_filters.FilterSet):
    #contacto_numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    class Meta:
        model = HumMotivoTerminacion        
        fields = {
            'id': ['exact', 'lte'],
        }