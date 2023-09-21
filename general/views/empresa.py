from rest_framework import viewsets, permissions
from general.models.empresa import Empresa
from general.serializers.empresa import EmpresaSerializador


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializador    
    permission_classes = [permissions.IsAuthenticated]