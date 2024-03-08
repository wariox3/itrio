from rest_framework import viewsets, permissions
from general.models.cuenta_banco import CuentaBanco
from general.serializers.cuenta_banco import CuentaBancoSerializador

class CuentaBancoViewSet(viewsets.ModelViewSet):
    queryset = CuentaBanco.objects.all()
    serializer_class = CuentaBancoSerializador
    permission_classes = [permissions.IsAuthenticated]