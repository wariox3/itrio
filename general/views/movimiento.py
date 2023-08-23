from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.documento import Documento
from general.serializers.documento import DocumentoSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializer
from general.serializers.documento_impuesto import DocumentoImpuestoSerializer
from rest_framework.decorators import action

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        documentos = Documento.objects.all()
        raw = request.data
        filtros = raw.get('filtro')
        if filtros:
            documentos.filter(nombre="mario")
            DocumentoSerializer = DocumentoSerializer(documentos, many=True)
            return Response(DocumentoSerializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        documentoSerializador = DocumentoSerializador(data=request.data)
        if documentoSerializador.is_valid():
            movimiento = DocumentoSerializador.save()            
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
                movimientoDetalleSerializador = DocumentoDetalleSerializer(data=datosMovimientoDetalle)
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
                        movimientoImpuestoSerializador = DocumentoImpuestoSerializer(data=datosMovimientoImpuesto)
                        if movimientoImpuestoSerializador.is_valid():
                            movimientoImpuestoSerializador.save() 
            return Response({'movimiento':documentoSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):
        try:
            raw = request.data
            codigoDocumento = raw.get('documento_id')
            if codigoDocumento:
                documento = Documento.objects.get(pk=codigoDocumento)
                return Response({'mensaje':'Se aprobo'}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje':'El movimiento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        
    def lista(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)
        cantidadLimite = raw.get('cantidad_limite', 5000)
        filtros = raw.get('filtros')
        ordenamientos = raw.get('ordenamientos')
        documentos = Documento.objects.all()
        if filtros:
            for filtro in filtros:
                documentos = documentos.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            documentos = documentos.order_by(*ordenamientos)
        documentos = documentos[desplazar:limite+desplazar]
        documentosCantidad = Documento.objects.all()[:cantidadLimite].count()
        DocumentoSerializer = DocumentoSerializer(documentos, many=True)
        return Response({"registros": DocumentoSerializer.data, "cantidad_registros": documentosCantidad}, status=status.HTTP_200_OK)