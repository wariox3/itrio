import django_filters
from general.models.documento_detalle import GenDocumentoDetalle
from django_filters import NumberFilter

class DocumentoDetalleFilter(django_filters.FilterSet):
    item__nombre = django_filters.CharFilter(field_name='item__nombre', lookup_expr='icontains')     
    documento__contacto__nombre_corto = django_filters.CharFilter(field_name='documento__contacto__nombre_corto', lookup_expr='icontains')    
    documento__contacto__numero_identificacion = django_filters.CharFilter(field_name='documento__contacto__numero_identificacion', lookup_expr='icontains')    
    documento__programacion_detalle__programacion_id = django_filters.NumberFilter(field_name='documento__programacion_detalle__programacion_id')
    inventario = django_filters.BooleanFilter(
        method='filtrar_inventario',
        label="Filtrar solo movimientos con efecto en inventario (1 o -1)"
    )
    cantidad_pendiente = django_filters.BooleanFilter(
        method='filtrar_cantidad_pendiente',
        label="Filtrar items con cantidad pendiente > 0"
    )    

    def filtrar_inventario(self, queryset, name, value):
        if value:
            return queryset.exclude(operacion_inventario=0)
        return queryset
    
    def filtrar_cantidad_pendiente(self, queryset, name, value):
        if value:
            return queryset.filter(cantidad_pendiente__gt=0)
        return queryset

    class Meta:
        model = GenDocumentoDetalle        
        fields = {
                    'id': ['exact', 'lte'],
                    'operacion_inventario': ['exact'],
                    'documento__estado_aprobado':['exact'],
                    'documento__numero':['exact', 'icontains'],
                    'documento__contacto__nombre_corto':['exact', 'icontains'],
                    'documento__contacto__numero_identificacion':['exact', 'icontains'],
                    'documento__documento_tipo__venta':['exact'],
                    'documento_id': ['exact'],
                    'documento_afectado_id': ['exact'],
                    'credito_id': ['exact'],
                    'item__nombre':['icontains'],
                    'documento__programacion_detalle__programacion_id': ['exact'],
                }