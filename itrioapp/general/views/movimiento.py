from rest_framework import viewsets, permissions
from general.models.movimiento import Movimiento
from general.serializers.movimiento import MovimientoSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
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