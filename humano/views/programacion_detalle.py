from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.programacion import HumProgramacion
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador
from humano.filters.programacion_detalle import ProgramacionDetalleFilter

class HumProgramacionDetalleViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacionDetalle.objects.all()
    serializer_class = HumProgramacionDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]   
    filterset_class = ProgramacionDetalleFilter 
    serializadores = {'lista': HumProgramacionDetalleSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumProgramacionDetalleSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset     

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        programacion = HumProgramacion.objects.get(pk=instance.programacion_id)
        
        if programacion.estado_aprobado:
            return Response({'mensaje': 'No se puede eliminar un documento aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        

        self.perform_destroy(instance)

        programacion.contratos = HumProgramacionDetalle.objects.filter(programacion_id=programacion.id).count()
        programacion.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
