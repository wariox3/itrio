import django_filters
from general.models.documento import GenDocumento
from django_filters import NumberFilter

class DocumentoFilter(django_filters.FilterSet):
    id__gte = NumberFilter(field_name='id', lookup_expr='gte')
    id__lte = NumberFilter(field_name='id', lookup_expr='lte')
    contacto_numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    class Meta:
        model = GenDocumento        
        fields = ['id',
                  'documento_tipo_id',
                  'numero', 
                  'contacto_numero_identificacion',
                  'estado_aprobado', 
                  'estado_anulado', 
                  'estado_electronico', 
                  'estado_contabilizado']