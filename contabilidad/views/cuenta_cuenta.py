from rest_framework import viewsets, permissions
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta
from contabilidad.serializers.cuenta_cuenta import ConCuentaCuentaSerializador

class CuentaCuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuentaCuenta.objects.all()
    serializer_class = ConCuentaCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]