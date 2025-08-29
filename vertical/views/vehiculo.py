from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.vehiculo import VerVehiculo
from vertical.models.viaje import VerViaje
from vertical.serializers.vehiculo import VerVehiculoSerializador


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = VerVehiculo.objects.all()
    serializer_class = VerVehiculoSerializador
    permission_classes = [permissions.IsAuthenticated]   