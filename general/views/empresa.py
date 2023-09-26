from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.empresa import Empresa
from general.serializers.empresa import EmpresaSerializador, EmpresaActualizarSerializador


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):        
        if Empresa.objects.filter(pk=2).exists():
            return Response({'mensaje':'Ya se creó la empresa', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            empresaSerializador = EmpresaSerializador(data=request.data)
            if empresaSerializador.is_valid():
                empresaSerializador.save()                         
                return Response({'empresa': empresaSerializador.data}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        empresa = self.get_object()
        empresaSerializador = EmpresaActualizarSerializador(empresa, data=request.data)
        if empresaSerializador.is_valid():
            empresaSerializador.save()
            return Response({'actualizacion': True, 'empresa': empresaSerializador.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion', 'codigo':23, 'validaciones': empresaSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)