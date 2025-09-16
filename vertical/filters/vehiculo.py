import django_filters
from vertical.models.vehiculo import VerVehiculo
class VerVehiculoFilter(django_filters.FilterSet):    

    class Meta:
        model = VerVehiculo
        fields = {  
                    'id': ['exact'],
                    'usuario_id': ['exact']
                }