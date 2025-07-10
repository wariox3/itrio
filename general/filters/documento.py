import django_filters
from general.models.documento import GenDocumento
from django_filters import NumberFilter

class DocumentoFilter(django_filters.FilterSet):
    contacto__numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    contacto__nombre_corto = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    documento_tipo__cobrar = django_filters.BooleanFilter(field_name='documento_tipo__cobrar')
    documento_tipo__pagar = django_filters.BooleanFilter(field_name='documento_tipo__pagar')
    documento_tipo__venta = django_filters.BooleanFilter(field_name='documento_tipo__venta')
    documento_tipo__electronico = django_filters.BooleanFilter(field_name='documento_tipo__electronico')
    documento_tipo__documento_clase_id = django_filters.NumberFilter(field_name='documento_tipo__documento_clase_id')
    documento_tipo__documento_clase__grupo = django_filters.NumberFilter(field_name='documento_tipo__documento_clase__grupo')
    documento_tipo__pos = django_filters.BooleanFilter(field_name='documento_tipo__pos')
    documento_tipo__contabilidad = django_filters.BooleanFilter(field_name='documento_tipo__contabilidad')
    class Meta:
        model = GenDocumento        
        fields = {'id': ['exact', 'lte'],
                  'contacto__nombre_corto':['icontains'],
                  'contacto__numero_identificacion':['icontains'],
                  'documento_tipo__pos': ['exact'],
                  'documento_tipo__contabilidad': ['exact'],
                  'documento_tipo_id': ['exact'],
                  'documento_tipo__documento_clase_id' : ['exact'],
                  'documento_tipo__nombre' : ['icontains'],
                  'documento_tipo__electronico' : ['exact'],
                  'documento_tipo__cobrar' : ['exact'],
                  'documento_tipo__pagar' : ['exact'],
                  'documento_tipo__venta' : ['exact'],
                  'documento_tipo__documento_clase__grupo' : ['exact'],
                  'contacto_id' : ['exact'],
                  'numero': ['exact', 'icontains'],                   
                  'fecha': ['gte', 'lte', 'gt', 'lt'], 
                  'fecha_hasta': ['gte', 'lte', 'gt', 'lt'], 
                  'pendiente': ['gt'],
                  'estado_aprobado': ['exact'], 
                  'estado_anulado': ['exact'], 
                  'estado_electronico': ['exact'], 
                  'estado_electronico_descartado': ['exact'], 
                  'estado_electronico_evento': ['exact'], 
                  'estado_contabilizado': ['exact'],
                  'programacion_detalle_id':['exact']}