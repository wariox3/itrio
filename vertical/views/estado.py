from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.estado import VerEstado
from vertical.serializers.estado import VerEstadoSerializador

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = VerEstado.objects.all()
    serializer_class = VerEstadoSerializador
    permission_classes = [permissions.IsAuthenticated]