from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.configuracion import GenConfiguracion
from general.serializers.configuracion import GenConfiguracionSerializador, GenConfiguracionActualizarSerializador

class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = GenConfiguracion.objects.all()
    serializer_class = GenConfiguracionSerializador    
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        pass
        
    def update(self, request, pk=None):
        configuracion = self.get_object()
        configuracionSerializador = GenConfiguracionActualizarSerializador(configuracion, data=request.data)
        if configuracionSerializador.is_valid():
            configuracionSerializador.save()
            return Response({'actualizacion': True, 'configuracion': configuracionSerializador.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion', 'codigo':23, 'validaciones': configuracionSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)