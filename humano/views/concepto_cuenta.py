from rest_framework import viewsets, permissions
from humano.models.concepto_cuenta import HumConceptoCuenta
from humano.serializers.concepto_cuenta import HumConceptoCuentaSerializador

class HumConceptoCuentaViewSet(viewsets.ModelViewSet):
    queryset = HumConceptoCuenta.objects.all()
    serializer_class = HumConceptoCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]