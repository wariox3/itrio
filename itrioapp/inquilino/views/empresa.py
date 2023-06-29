from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from inquilino.models import Empresa
from inquilino.serializers import EmpresaSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer    
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'consulta-subdominio',)
    def all_post_author(self, request):
        try:
            nombre = request.data.get('nombre')
            empresa = Empresa.objects.get(schema_name=nombre)
            serializer = EmpresaSerializer(empresa)
            return Response({'empresa':serializer.data}, status=status.HTTP_200_OK)    
        except Empresa.DoesNotExist:
            return Response({'mensaje':'No existe el registro', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)