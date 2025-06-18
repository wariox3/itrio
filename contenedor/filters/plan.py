import django_filters
from contenedor.models import CtnPlan

class PlanFilter(django_filters.FilterSet):    
    class Meta:
        model = CtnPlan
        fields = {'id': ['exact'],
                  'nombre': ['exact','icontains']}