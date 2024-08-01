from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from humano.models.hum_contrato import HumContrato
from humano.serializers.hum_contrato import HumContratoSerializador
from django.db.models.deletion import ProtectedError

class HumMovimientoViewSet(viewsets.ModelViewSet):
    queryset = HumContrato.objects.all()
    serializer_class = HumContratoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            return Response({'mensaje':'El contrato tiene relaciones', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)   

    def perform_destroy(self, instance):
        instance.delete()    