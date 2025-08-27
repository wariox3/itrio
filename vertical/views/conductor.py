from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.conductor import VerConductor
from vertical.serializers.conductor import VerConductorSerializador

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = VerConductor.objects.all()
    serializer_class = VerConductorSerializador
    permission_classes = [permissions.IsAuthenticated]