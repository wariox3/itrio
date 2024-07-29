from rest_framework import viewsets, permissions
from contabilidad.models.con_cuenta import ConCuenta
from contabilidad.serializers.cuenta import CuentaSerializer

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]