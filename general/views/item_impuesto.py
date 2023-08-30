from rest_framework import viewsets, permissions
from general.models.item_impuesto import ItemImpuesto
from general.serializers.item_impuesto import ItemImpuestoSerializador

class ItemImpuestoViewSet(viewsets.ModelViewSet):
    queryset = ItemImpuesto.objects.all()
    serializer_class = ItemImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]