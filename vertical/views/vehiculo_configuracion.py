from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.vehiculo_configuracion import VerVehiculoConfiguracion
from vertical.serializers.vehiculo_configuracion import VerVehiculoConfiguracionSerializador

class VehiculoConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = VerVehiculoConfiguracion.objects.all()
    serializer_class = VerVehiculoConfiguracionSerializador
    permission_classes = [permissions.IsAuthenticated]