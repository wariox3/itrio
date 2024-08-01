from rest_framework import viewsets, permissions
from contabilidad.models.cuenta import ConCuenta
from contabilidad.serializers.cuenta import ConCuentaSerializador

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuenta.objects.all()
    serializer_class = ConCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]