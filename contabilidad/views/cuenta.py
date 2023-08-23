from rest_framework import viewsets, permissions
from contabilidad.models.cuenta import Cuenta
from contabilidad.serializers.cuenta import CuentaSerializer

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]