from rest_framework import viewsets, permissions
from seguridad.models import UsuarioEmpresa
from seguridad.serializers import UsuarioEmpresaSerializador


class UsuarioEmpresaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioEmpresa.objects.all()
    serializer_class = UsuarioEmpresaSerializador    
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        pass