import django_filters
from transporte.models.despacho import TteDespacho

class DespachoFilter(django_filters.FilterSet):    
    ciudad_origen__nombre = django_filters.CharFilter(field_name='ciudad_origen__nombre', lookup_expr='icontains')
    ciudad_destino__nombre = django_filters.CharFilter(field_name='ciudad_destino__nombre', lookup_expr='icontains')  
    class Meta:
        model = TteDespacho
        fields = {'id': ['exact'],
                  'ciudad_origen__nombre' : ['icontains'],
                  'ciudad_origen_id': ['exact'],
                  'ciudad_destino__nombre' : ['icontains'],
                  'ciudad_destino_id': ['exact'],
                  'ruta_id': ['exact'],
                  'operacion_id': ['exact'],
                  'conductor_id': ['exact'],
                  'vehiculo_id': ['exact'],
                  'remolque_id': ['exact'],
                  }