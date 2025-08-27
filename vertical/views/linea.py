from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.linea import VerLinea
from vertical.serializers.linea import VerLineaSerializador

class LineaViewSet(viewsets.ModelViewSet):
    queryset = VerLinea.objects.all()
    serializer_class = VerLineaSerializador
    permission_classes = [permissions.IsAuthenticated]