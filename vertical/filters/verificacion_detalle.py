import django_filters
from vertical.models.verificacion_detalle import VerVerificacionDetalle
class VerVerificacionDetalleFilter(django_filters.FilterSet):    

    class Meta:
        model = VerVerificacionDetalle
        fields = {  
                    'id': ['exact'],
                    'verificacion_id': ['exact'],
                }