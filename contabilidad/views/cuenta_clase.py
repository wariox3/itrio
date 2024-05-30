from rest_framework import viewsets, permissions
from contabilidad.models.cuenta_clase import CuentaClase
from contabilidad.serializers.cuenta_clase import CuentaClaseSerializer

class CuentaClaseViewSet(viewsets.ModelViewSet):
    queryset = CuentaClase.objects.all()
    serializer_class = CuentaClaseSerializer
    permission_classes = [permissions.IsAuthenticated]