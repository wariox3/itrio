from rest_framework import viewsets, permissions
from contabilidad.models.con_cuenta_clase import ConCuentaClase
from contabilidad.serializers.cuenta_clase import CuentaClaseSerializer

class CuentaClaseViewSet(viewsets.ModelViewSet):
    queryset = ConCuentaClase.objects.all()
    serializer_class = CuentaClaseSerializer
    permission_classes = [permissions.IsAuthenticated]