import django_filters
from contenedor.models import CtnRegimen

class RegimenFilter(django_filters.FilterSet):    
    class Meta:
        model = CtnRegimen
        fields = {
            'id': ['exact', 'lte']}