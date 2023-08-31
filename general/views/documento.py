from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.serializers.documento import DocumentoSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializer
from rest_framework.decorators import action

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        pass

    def create(self, request):
        raw = request.data
        documentoSerializador = DocumentoSerializador(data=raw)
        if documentoSerializador.is_valid():
            documento = documentoSerializador.save()            
            detalles = raw.get('detalles')
            for detalle in detalles:                
                detalle['documento'] = documento.id
                detalleSerializador = DocumentoDetalleSerializador(data=detalle)
                if detalleSerializador.is_valid():
                    documentoDetalle = detalleSerializador.save() 
                    """impuestos = detalle.get('impuestos')
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
                            documentoImpuestoSerializador.save()""" 
                else:
                    return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
            documentoDetalles = DocumentoDetalle.objects.filter(documento=documento.id)
            documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
            documentoRespuesta = documentoSerializador.data
            documentoRespuesta['detalles'] = documentoDetallesSerializador.data
            return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Documento.objects.all()
        documento = get_object_or_404(queryset, pk=pk)
        documentoSerializador = DocumentoSerializador(documento)
        documentoDetalles = DocumentoDetalle.objects.filter(documento=pk)
        documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
        documentoRespuesta = documentoSerializador.data
        documentoRespuesta['detalles'] = documentoDetallesSerializador.data
        return Response({'documento':documentoRespuesta}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        raw = request.data
        documento = Documento.objects.get(pk=pk)
        documentoSerializador = DocumentoSerializador(documento, data=raw, partial=True)
        if documentoSerializador.is_valid():
            documentoSerializador.save()
            detalles = raw.get('detalles')
            if detalles is not None:
                for detalle in detalles:                
                    if detalle.get('id'):
                        documentoDetalle = DocumentoDetalle.objects.get(pk=detalle['id'])
                        detalleSerializador = DocumentoDetalleSerializador(documentoDetalle, data=detalle, partial=True)    
                    else:
                        detalle['documento'] = documento.id
                        detalleSerializador = DocumentoDetalleSerializador(data=detalle)
                    if detalleSerializador.is_valid():
                        detalleSerializador.save() 
                    else:
                        return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
            detallesEliminados = raw.get('detalles_eliminados')
            if detallesEliminados is not None:
                for detalle in detallesEliminados:                                
                    documentoDetalle = DocumentoDetalle.objects.get(pk=detalle)
                    documentoDetalle.delete()
            documentoDetalles = DocumentoDetalle.objects.filter(documento=pk)
            documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
            documentoRespuesta = documentoSerializador.data
            documentoRespuesta['detalles'] = documentoDetallesSerializador.data                    
            return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)                    
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        codigoDocumentoTipo = raw.get('documento_tipo_id')
        if codigoDocumentoTipo:
            desplazar = raw.get('desplazar', 0)
            limite = raw.get('limite', 50)    
            limiteTotal = raw.get('limite_total', 5000)                
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')                         
            documentos = Documento.objects.all()
            if filtros:
                for filtro in filtros:
                    documentos = documentos.filter(**{filtro['propiedad']: filtro['valor_1']})
            if ordenamientos:
                documentos = documentos.order_by(*ordenamientos)              
            documentos = documentos[desplazar:limite+desplazar]
            itemsCantidad = Documento.objects.all()[:limiteTotal].count()
            serializador = DocumentoSerializador(documentos, many=True) 
            fields_info = []
            model_fields = DocumentoSerializador().get_fields()
            for field_name, field_instance in model_fields.items():
                field_type = field_instance.__class__.__name__
                fields_info.append({"nombre": field_name, "tipo": field_type})       
            return Response({"propiedades":fields_info, "registros": serializador.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

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
            codigoDocumento = raw.get('id')
            if codigoDocumento:
                documento = Documento.objects.get(pk=codigoDocumento)
                documento.estado_aprobado = True
                documento.save()
                return Response({'estado_aprobado': True}, status=status.HTTP_200_OK)
            else:
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'excel',)
    def excel(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = raw.get('filtros')
        ordenamientos = raw.get('ordenamientos')  
        prueba = self.lista(desplazar, limite, limiteTotal, filtros, ordenamientos)
        return Response({'prueba': prueba}, status=status.HTTP_200_OK)        
    
    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        return "hola mundo"