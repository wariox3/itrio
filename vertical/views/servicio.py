from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.servicio import VerServicio
from vertical.serializers.servicio import VerServicioSerializador

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = VerServicio.objects.all()
    serializer_class = VerServicioSerializador
    permission_classes = [permissions.IsAuthenticated]