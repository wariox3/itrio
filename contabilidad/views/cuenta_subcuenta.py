from rest_framework import viewsets, permissions
from contabilidad.models.cuenta_subcuenta import ConCuentaSubcuenta
from contabilidad.serializers.cuenta_subcuenta import ConCuentaSubcuentaSerializador

class CuentaSubcuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuentaSubcuenta.objects.all()
    serializer_class = ConCuentaSubcuentaSerializador
    permission_classes = [permissions.IsAuthenticated]