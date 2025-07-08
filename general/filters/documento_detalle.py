import django_filters
from general.models.documento_detalle import GenDocumentoDetalle
from django_filters import NumberFilter

class DocumentoDetalleFilter(django_filters.FilterSet):
    item__nombre = django_filters.CharFilter(field_name='item__nombre', lookup_expr='icontains')     
    documento__contacto__nombre_corto = django_filters.CharFilter(field_name='documento__contacto__nombre_corto', lookup_expr='icontains')    
    documento__contacto__numero_identificacion = django_filters.CharFilter(field_name='documento__contacto__numero_identificacion', lookup_expr='icontains')    
    class Meta:
        model = GenDocumentoDetalle        
        fields = {
                    'id': ['exact', 'lte'],
                    'operacion_inventario': ['exact', 'exclude'],
                    'documento__estado_aprobado':['exact'],
                    'documento__numero':['exact', 'icontains'],
                    'documento__contacto__nombre_corto':['exact', 'icontains'],
                    'documento__contacto__numero_identificacion':['exact', 'icontains'],
                    'documento__documento_tipo__venta':['exact'],
                    'documento_id': ['exact'],
                    'item__nombre':['icontains'],
                }