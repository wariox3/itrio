import django_filters
from general.models.documento import GenDocumento

class DocumentoFilter(django_filters.FilterSet):
    contacto_numero_identificacion = django_filters.CharFilter(field_name='contacto__numero_identificacion', lookup_expr='icontains')
    class Meta:
        model = GenDocumento        
        fields = ['documento_tipo_id','numero', 'contacto_numero_identificacion',
                    'estado_aprobado', 'estado_anulado', 'estado_electronico', 'estado_contabilizado']