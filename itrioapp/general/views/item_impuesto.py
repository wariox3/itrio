from rest_framework import viewsets, permissions
from general.models.item_impuesto import ItemImpuesto
from general.serializers.item_impuesto import ItemImpuestoSerializer

class ItemImpuestoViewSet(viewsets.ModelViewSet):
    queryset = ItemImpuesto.objects.all()
    serializer_class = ItemImpuestoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def handle_exception(self, exc):
        response = super().handle_exception(exc)

        if response is None:
            return None

        if response.status_code == 400:
            response.data = {
                'mensaje': 'Mensajes de validacion',
                'codigo': 14,
                'validacion': response.data
            }

        return response