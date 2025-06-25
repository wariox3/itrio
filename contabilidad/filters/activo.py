import django_filters
from contabilidad.models.activo import ConActivo

class ActivoFilter(django_filters.FilterSet):    
    class Meta:
        model = ConActivo
        fields = {'id': ['exact']}