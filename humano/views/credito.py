from rest_framework import viewsets, permissions
from humano.models.credito import HumCredito
from humano.serializers.credito import HumCreditoSerializador

class HumCreditoViewSet(viewsets.ModelViewSet):
    queryset = HumCredito.objects.all()
    serializer_class = HumCreditoSerializador
    permission_classes = [permissions.IsAuthenticated]