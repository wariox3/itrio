from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.ciudad import VerCiudad
from vertical.serializers.ciudad import VerCiudadSerializador

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = VerCiudad.objects.all()
    serializer_class = VerCiudadSerializador
    permission_classes = [permissions.IsAuthenticated]