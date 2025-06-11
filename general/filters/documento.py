import django_filters
from general.models.documento import GenDocumento
from django_filters import NumberFilter

class DocumentoFilter(django_filters.FilterSet):
    contacto_numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    documento_tipo__cobrar = django_filters.BooleanFilter(field_name='documento_tipo__cobrar')
    documento_tipo__pagar = django_filters.BooleanFilter(field_name='documento_tipo__cobrar')
    documento_tipo__documento_clase_id = django_filters.NumberFilter(field_name='documento_tipo__documento_clase_id')
    class Meta:
        model = GenDocumento        
        fields = {'id': ['exact', 'lte'],
                  'documento_tipo_id': ['exact'],
                  'numero': ['exact'], 
                  'pendiente': ['gt'],
                  'estado_aprobado': ['exact'], 
                  'estado_anulado': ['exact'], 
                  'estado_electronico': ['exact'], 
                  'estado_contabilizado': ['exact']}