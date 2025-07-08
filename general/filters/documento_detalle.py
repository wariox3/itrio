import django_filters
from general.models.documento_detalle import GenDocumentoDetalle
from django_filters import NumberFilter

class DocumentoDetalleFilter(django_filters.FilterSet):
    item__nombre = django_filters.CharFilter(field_name='item__nombre', lookup_expr='icontains')     
    class Meta:
        model = GenDocumentoDetalle        
        fields = {'id': ['exact', 'lte'],
                  'documento__estado_aprobado':['exact'],
                  'documento__documento_tipo__venta':['exact'],
                  'documento_id': ['exact'],
                  'item__nombre':['icontains'],}