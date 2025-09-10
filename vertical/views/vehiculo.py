from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.vehiculo import VerVehiculo
from vertical.models.viaje import VerViaje
from vertical.serializers.vehiculo import VerVehiculoSerializador, VerVehiculoSeleccionarSerializador


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = VerVehiculo.objects.all()
    serializer_class = VerVehiculoSerializador
    permission_classes = [permissions.IsAuthenticated] 

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        placa = request.query_params.get('placa__icontains', None)
        queryset = self.get_queryset()
        if placa:
            queryset = queryset.filter(placa__icontains=placa)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = VerVehiculoSeleccionarSerializador(queryset, many=True)        
        return Response(serializer.data)       