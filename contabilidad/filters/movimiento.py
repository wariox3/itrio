import django_filters
from contabilidad.models.movimiento import ConMovimiento

class MovimientoFilter(django_filters.FilterSet):   
    cuenta__codigo = django_filters.CharFilter(field_name='cuenta__codigo', lookup_expr='icontains') 
    contacto__numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    contacto__nombre_corto = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    grupo__nombre = django_filters.CharFilter(field_name='grupo__nombre', lookup_expr='icontains')
    class Meta:
        model = ConMovimiento
        fields = {
                    'id': ['exact'],
                    'documento_id': ['exact'],
                    'grupo_id': ['exact'],
                    'cuenta__codigo': ['icontains'],
                    'contacto__nombre_corto':['icontains'],
                    'contacto__numero_identificacion':['icontains'],
                    'grupo__nombre':['icontains'],
                    'fecha': ['gte', 'lte', 'gt', 'lt', 'exact'],
                    'numero':['icontains', 'exact'],
                }