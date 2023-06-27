from rest_framework import viewsets, permissions
from inquilino.models import Empresa
from inquilino.serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer    
    permission_classes = [permissions.IsAuthenticated]