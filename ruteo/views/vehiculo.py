from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ruteo.models.vehiculo import RutVehiculo
from ruteo.serializers.vehiculo import RutVehiculoSerializador
import base64
from io import BytesIO
import openpyxl
from datetime import datetime

class RutVehiculoViewSet(viewsets.ModelViewSet):
    queryset = RutVehiculo.objects.all()
    serializer_class = RutVehiculoSerializador
    permission_classes = [permissions.IsAuthenticated]