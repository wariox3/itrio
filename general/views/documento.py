from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from general.models.documento import Documento
from general.serializers.documento import DocumentoSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializer
from general.serializers.documento_impuesto import DocumentoImpuestoSerializer
from rest_framework.decorators import action

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        raw = request.data
        documentoSerializador = DocumentoSerializador(data=raw)
        if documentoSerializador.is_valid():
            documento = documentoSerializador.save()            
            detalles = raw.get('detalles')
            for detalle in detalles:                
                datosDetalle = {
                    "documento":documento.id, 
                    "item":detalle['item'], 
                    "cantidad":detalle['cantidad'],
                    "precio":detalle['precio'],                    
                    "porcentaje_descuento":detalle['porcentaje_descuento'],
                    "descuento":detalle['descuento'],
                    "subtotal":detalle['subtotal'],
                    "total_bruto":detalle['total_bruto'],
                    "total":detalle['total']
                }
                detalleSerializador = DocumentoDetalleSerializer(data=datosDetalle)
                if detalleSerializador.is_valid():
                    documentoDetalle = detalleSerializador.save() 
                    impuestos = detalle.get('impuestos')
                    for impuesto in impuestos:
                        datosDocumentoImpuesto = {
                            "documento_detalle":documentoDetalle.id, 
                            "impuesto":impuesto['impuesto'],
                            "base":impuesto['base'],
                            "porcentaje":impuesto['porcentaje'],
                            "total":impuesto['total']
                        }
                        documentoImpuestoSerializador = DocumentoImpuestoSerializer(data=datosDocumentoImpuesto)
                        if documentoImpuestoSerializador.is_valid():
                            documentoImpuestoSerializador.save() 
            return Response({'documento': documentoSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'eliminar',)
    def eliminar(self, request):
        try:
            raw = request.data
            documentos = raw.get('documentos')
            if documentos:  
                for documento in documentos:
                    documentoEliminar = Documento.objects.get(pk=documento)  
                    if documentoEliminar:
                        documentoEliminar.delete()   
                return Response({'mensaje':'Registros eliminados'}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)

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