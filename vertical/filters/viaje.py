import django_filters
from vertical.models.viaje import VerViaje
class VerViajeFilter(django_filters.FilterSet):    

    class Meta:
        model = VerViaje
        fields = {  
                    'id': ['exact'],
                    'solicitud_cliente': ['exact'],
                    'estado_aceptado': ['exact'],
                }