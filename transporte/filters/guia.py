import django_filters
from transporte.models.guia import TteGuia

class GuiaFilter(django_filters.FilterSet):    
    ciudad_origen__nombre = django_filters.CharFilter(field_name='ciudad_origen__nombre', lookup_expr='icontains')
    ciudad_destino__nombre = django_filters.CharFilter(field_name='ciudad_destino__nombre', lookup_expr='icontains')
    class Meta:
        model = TteGuia
        fields = {'id': ['exact'],
                  'estado_despachado': ['exact'],
                  'estado_entregado': ['exact'],
                  'estado_facturado': ['exact'],
                  'ciudad_origen__nombre' : ['icontains'],
                  'ciudad_origen_id': ['exact'],
                  'ciudad_destino__nombre' : ['icontains'],
                  'ciudad_destino_id': ['exact'],
                  'fecha': ['gte', 'lte', 'gt', 'lt', 'exact'], 
                  'contacto_id': ['exact'],
                  }