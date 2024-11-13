from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.flota import RutFlota
from ruteo.serializers.flota import RutFlotaSerializador

class RutFlotaViewSet(viewsets.ModelViewSet):
    queryset = RutFlota.objects.all()
    serializer_class = RutFlotaSerializador
    permission_classes = [permissions.IsAuthenticated]                 