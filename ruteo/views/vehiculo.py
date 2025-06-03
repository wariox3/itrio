from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from ruteo.models.vehiculo import RutVehiculo
from ruteo.models.franja import RutFranja
from ruteo.serializers.vehiculo import RutVehiculoSerializador

class RutVehiculoViewSet(viewsets.ModelViewSet):
    queryset = RutVehiculo.objects.all()
    serializer_class = RutVehiculoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        franja_codigos = request.data.pop('franja_codigo', [])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehiculo = serializer.save()
        
        for codigo in franja_codigos:
            try:
                franja = RutFranja.objects.get(pk=codigo)
                vehiculo.franjas.add(franja)
            except RutFranja.DoesNotExist:
                pass
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        franja_codigos = request.data.pop('franja_codigo', [])
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        vehiculo = serializer.save()
        
        vehiculo.franjas.clear()
        for codigo in franja_codigos:
            try:
                franja = RutFranja.objects.get(pk=codigo)
                vehiculo.franjas.add(franja)
            except RutFranja.DoesNotExist:
                pass
        
        return Response(serializer.data)