from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.contrato import HumContrato
from humano.serializers.contrato import HumContratoSerializador
from django.db.models.deletion import ProtectedError
from datetime import datetime

class HumMovimientoViewSet(viewsets.ModelViewSet):
    queryset = HumContrato.objects.all()
    serializer_class = HumContratoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raw = request.data        
        contacto_id = raw.get('contacto')
        contrato_activo = HumContrato.objects.filter(contacto_id=contacto_id, estado_terminado=False).exists()    
        if contrato_activo:
            return Response({'mensaje':'El contacto ya tiene un contrato activo', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response({'mensaje':'Contrato eliminado'}, status=status.HTTP_200_OK)
        except ProtectedError as e:
            return Response({'mensaje':'El contrato tiene relaciones', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)   

    def perform_destroy(self, instance):
        instance.delete()    

    @action(detail=False, methods=["post"], url_path=r'terminar',)
    def terminar(self, request):
        raw = request.data
        id = raw.get('id')
        fecha_terminacion = raw.get('fecha_terminacion')
        if id and fecha_terminacion:
            try:
                contrato = HumContrato.objects.get(pk=id)
                if contrato.estado_terminado == False:
                    fecha_terminacion = datetime.strptime(fecha_terminacion, '%Y-%m-%d').date()
                    if fecha_terminacion > contrato.fecha_desde:
                        contrato.fecha_hasta = fecha_terminacion
                        contrato.estado_terminado = True
                        contrato.save()
                        return Response({'mensaje': 'Contrato finalizado'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'mensaje':'No puede terminar el contrato antes de su inicio', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'El contrato ya esta terminado', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except HumContrato.DoesNotExist:
                return Response({'mensaje':'El contrato no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)         