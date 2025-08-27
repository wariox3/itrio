from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.pais import VerPais
from vertical.serializers.pais import VerPaisSerializador

class PaisViewSet(viewsets.ModelViewSet):
    queryset = VerPais.objects.all()
    serializer_class = VerPaisSerializador
    permission_classes = [permissions.IsAuthenticated]