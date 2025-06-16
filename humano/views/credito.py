from rest_framework import viewsets, permissions
from humano.models.credito import HumCredito
from humano.serializers.credito import HumCreditoSerializador

class HumCreditoViewSet(viewsets.ModelViewSet):
    queryset = HumCredito.objects.all()
    serializer_class = HumCreditoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        total = serializer.validated_data.get('total')
        serializer.save(saldo=total)

    def perform_update(self, serializer):
        total = serializer.validated_data.get('total')
        abono = serializer.validated_data.get('abono', serializer.instance.abono)
        saldo = total - abono
        serializer.save(saldo=saldo)