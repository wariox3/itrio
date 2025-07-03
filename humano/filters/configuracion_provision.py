import django_filters
from humano.models.configuracion_provision import HumConfiguracionProvision

class ConfiguracionProvisionFilter(django_filters.FilterSet):
    class Meta:
        model = HumConfiguracionProvision        
        fields = {'id': ['exact', 'lte'],
                  'orden':['exact']}