from rest_framework import viewsets, permissions
from general.models.impuesto import GenImpuesto
from general.serializers.impuesto import GenImpuestoSerializador

class ImpuestoViewSet(viewsets.ModelViewSet):
    queryset = GenImpuesto.objects.all()
    serializer_class = GenImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]  