from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.categoria_licencia import VerCategoriaLicencia
from vertical.serializers.categoria_licencia import VerCategoriaLicenciaSerializador

class CategoriaLicenciaViewSet(viewsets.ModelViewSet):
    queryset = VerCategoriaLicencia.objects.all()
    serializer_class = VerCategoriaLicenciaSerializador
    permission_classes = [permissions.IsAuthenticated]