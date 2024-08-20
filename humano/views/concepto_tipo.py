from rest_framework import viewsets, permissions
from humano.models.concepto_tipo import HumConceptoTipo
from humano.serializers.concepto_tipo import HumConceptoTipoSerializador

class HumConceptoTipoViewSet(viewsets.ModelViewSet):
    queryset = HumConceptoTipo.objects.all()
    serializer_class = HumConceptoTipoSerializador
    permission_classes = [permissions.IsAuthenticated]