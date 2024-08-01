from rest_framework import viewsets, permissions
from general.models.item_impuesto import ItemImpuesto
from general.serializers.item_impuesto import GenItemImpuestoSerializador

class ItemImpuestoViewSet(viewsets.ModelViewSet):
    queryset = ItemImpuesto.objects.all()
    serializer_class = GenItemImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]