import django_filters
from crm.models.presupuesto import CrmPresupuesto
from django_filters import NumberFilter

class PresupuestoFilter(django_filters.FilterSet):
    contacto__numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    contacto__nombre_corto = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    class Meta:
        model = CrmPresupuesto        
        fields = {'id': ['exact', 'lte'],
                  'contacto__nombre_corto':['icontains'],
                  'contacto__numero_identificacion':['icontains']}