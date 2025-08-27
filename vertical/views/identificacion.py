from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.identificacion import VerIdentificacion
from vertical.serializers.identificacion import VerIdentificacionSerializador

class IdentificacionViewSet(viewsets.ModelViewSet):
    queryset = VerIdentificacion.objects.all()
    serializer_class = VerIdentificacionSerializador
    permission_classes = [permissions.IsAuthenticated]