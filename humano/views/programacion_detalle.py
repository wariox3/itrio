from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.programacion import HumProgramacion
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador

class HumProgramacionDetalleViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacionDetalle.objects.all()
    serializer_class = HumProgramacionDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]       

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        programacion = HumProgramacion.objects.get(pk=instance.programacion_id)
        if programacion.estado_aprobado:
                return Response({'mensaje': 'No se puede eliminar un documento aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        
        programacion.contratos -= 1
        programacion.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    