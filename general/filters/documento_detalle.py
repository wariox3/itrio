import django_filters
from general.models.documento_detalle import GenDocumentoDetalle
from django_filters import NumberFilter

class DocumentoDetalleFilter(django_filters.FilterSet):     
    class Meta:
        model = GenDocumentoDetalle        
        fields = {'id': ['exact', 'lte'],
                  'documento__estado_aprobado':['exact'],
                  'documento__documento_tipo__venta':['exact']}