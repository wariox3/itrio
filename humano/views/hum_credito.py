from rest_framework import viewsets, permissions
from humano.models.hum_credito import HumCredito
from humano.serializers.hum_credito import HumCreditoSerializador

class HumCreditoViewSet(viewsets.ModelViewSet):
    queryset = HumCredito.objects.all()
    serializer_class = HumCreditoSerializador
    permission_classes = [permissions.IsAuthenticated]