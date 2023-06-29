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
    def consulta_subdominio(self, request):
        try:
            subdominio = request.data.get('subdominio')
            empresa = Empresa.objects.get(schema_name=subdominio)
            serializer = EmpresaSerializer(empresa)
            return Response({'empresa':serializer.data}, status=status.HTTP_200_OK)    
        except Empresa.DoesNotExist:
            return Response({'mensaje':'No existe el registro', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        try:
            subdominio = request.data.get('subdominio')
            Empresa.objects.get(schema_name=subdominio)
            return Response({'validar':False}, status=status.HTTP_200_OK)    
        except Empresa.DoesNotExist:
            return Response({'validar':True}, status=status.HTTP_200_OK)        