from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.combustible import VerCombustible
from vertical.serializers.combustible import VerCombustibleSerializador

class CombustibleViewSet(viewsets.ModelViewSet):
    queryset = VerCombustible.objects.all()
    serializer_class = VerCombustibleSerializador
    permission_classes = [permissions.IsAuthenticated]