from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.marca import VerMarca
from vertical.serializers.marca import VerMarcaSerializador

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = VerMarca.objects.all()
    serializer_class = VerMarcaSerializador
    permission_classes = [permissions.IsAuthenticated]