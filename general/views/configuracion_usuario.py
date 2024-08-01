from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.configuracion_usuario import ConfiguracionUsuario
from general.serializers.configuracion_usuario import GenConfiguracionUsuarioSerializador, GenConfiguracionUsuarioActualizarSerializador

class ConfiguracionUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionUsuario.objects.all()
    serializer_class = GenConfiguracionUsuarioActualizarSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        pass
        
    def update(self, request, pk=None):
        configuracionUsuario = self.get_object()
        configuracionUsuarioSerializador = GenConfiguracionUsuarioActualizarSerializador(configuracionUsuario, data=request.data)
        if configuracionUsuarioSerializador.is_valid():
            configuracionUsuarioSerializador.save()
            return Response({'actualizacion': True, 'configuracion': configuracionUsuarioSerializador.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion', 'codigo':23, 'validaciones': configuracionUsuarioSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)