from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from humano.models.contrato import HumContrato
from humano.serializers.contrato import HumContratoSerializador
from django.db.models.deletion import ProtectedError

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