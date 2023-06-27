from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.movimiento import Movimiento
from general.serializers.movimiento import MovimientoSerializer
from general.serializers.movimiento_detalle import MovimientoDetalleSerializer
from general.serializers.movimiento_impuesto import MovimientoImpuestoSerializer

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
                    "cantidad":detalle['cantidad'],
                    "precio":detalle['precio'],                    
                    "porcentaje_descuento":detalle['porcentaje_descuento'],
                    "descuento":detalle['descuento'],
                    "subtotal":detalle['subtotal'],
                    "total_bruto":detalle['total_bruto'],
                    "total":detalle['total']
                }
                movimientoDetalleSerializador = MovimientoDetalleSerializer(data=datosMovimientoDetalle)
                if movimientoDetalleSerializador.is_valid():
                    movimientoDetalle = movimientoDetalleSerializador.save() 
                    impuestos = detalle.get('impuestos')
                    for impuesto in impuestos:
                        datosMovimientoImpuesto = {
                            "movimiento_detalle":movimientoDetalle.id, 
                            "impuesto":impuesto['impuesto'],
                            "base":impuesto['base'],
                            "porcentaje":impuesto['porcentaje'],
                            "total":impuesto['total']
                        }
                        movimientoImpuestoSerializador = MovimientoImpuestoSerializer(data=datosMovimientoImpuesto)
                        if movimientoImpuestoSerializador.is_valid():
                            movimientoImpuestoSerializador.save() 
            return Response({'movimiento':movimientoSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': movimientoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)