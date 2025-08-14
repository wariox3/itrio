import django_filters
from transporte.models.vehiculo import TteVehiculo

class RutaFilter(django_filters.FilterSet):    
    
    class Meta:
        model = TteVehiculo
        fields = {'id': ['exact'],
                'placa': ['exact', 'icontains'],                        
                  }