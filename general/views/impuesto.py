from rest_framework import viewsets, permissions
from general.models.impuesto import Impuesto
from general.serializers.impuesto import GenImpuestoSerializador

class ImpuestoViewSet(viewsets.ModelViewSet):
    queryset = Impuesto.objects.all()
    serializer_class = GenImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]  