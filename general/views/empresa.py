from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.empresa import Empresa
from general.serializers.empresa import EmpresaSerializador


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):        
        if Empresa.objects.filter(pk=1).exists():
            return Response({'mensaje':'Ya se creó la empresa', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            empresaSerializador = EmpresaSerializador(data=request.data)
            if empresaSerializador.is_valid():
                empresaSerializador.save()                         
                return Response({'empresa': empresaSerializador.data}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)    