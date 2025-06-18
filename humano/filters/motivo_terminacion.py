import django_filters
from humano.models.motivo_terminacion import HumMotivoTerminacion

class MotivoTerminacionFilter(django_filters.FilterSet):

    class Meta:
        model = HumMotivoTerminacion        
        fields = {
            'id': ['exact', 'lte'],
        }