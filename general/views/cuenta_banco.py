from rest_framework import viewsets, permissions
from general.models.cuenta_banco import GenCuentaBanco
from general.serializers.cuenta_banco import GenCuentaBancoSerializador

class CuentaBancoViewSet(viewsets.ModelViewSet):
    queryset = GenCuentaBanco.objects.all()
    serializer_class = GenCuentaBancoSerializador
    permission_classes = [permissions.IsAuthenticated]