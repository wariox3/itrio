from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.vehiculo import VerVehiculo
from vertical.serializers.vehiculo import VerVehiculoSerializador, VerVehiculoSeleccionarSerializador
from vertical.filters.vehiculo import VerVehiculoFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = VerVehiculo.objects.all()
    serializer_class = VerVehiculoSerializador
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VerVehiculoFilter

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        placa = request.query_params.get('placa__icontains', None)
        usuario_id = request.query_params.get('usuario_id', None)
        if usuario_id:
            queryset = self.get_queryset()
            queryset.filter(usuario_id=usuario_id)
            if placa:
                queryset = queryset.filter(placa__icontains=placa)
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                pass    
            serializer = VerVehiculoSeleccionarSerializador(queryset, many=True)        
            return Response(serializer.data)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)