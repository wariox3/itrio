from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.movimiento import Movimiento
from general.serializers.movimiento import MovimientoSerializer
from general.serializers.Movimiento_detalle import MovimientoDetalleSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        data = request.data
        movimientoSerializador = MovimientoSerializer(data=request.data)
        if movimientoSerializador.is_valid():
            movimiento = movimientoSerializador.save()            
            detalles = data.get('detalles')
            for detalle in detalles:                
                datosMovimientoDetalle = {
                    "movimiento":movimiento.id, 
                    "item":detalle['item'], 
                    "cantidad":detalle['cantidad']
                    }
                movimientoDetalleSerializador = MovimientoDetalleSerializer(data=datosMovimientoDetalle)
                if movimientoDetalleSerializador.is_valid():
                    movimientoDetalleSerializador.save() 
            return Response({'movimiento':movimientoSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': movimientoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

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