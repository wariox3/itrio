from rest_framework import viewsets, permissions
from contabilidad.models.cuenta_clase import ConCuentaClase
from contabilidad.serializers.cuenta_clase import ConCuentaClaseSerializador

class CuentaClaseViewSet(viewsets.ModelViewSet):
    queryset = ConCuentaClase.objects.all()
    serializer_class = ConCuentaClaseSerializador
    permission_classes = [permissions.IsAuthenticated]