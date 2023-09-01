from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.models.documento_impuesto import DocumentoImpuesto
from general.serializers.documento import DocumentoSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializador
from openpyxl import Workbook
from reportlab.pdfgen import canvas

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
            if detalles is not None:
                for detalle in detalles:                
                    detalle['documento'] = documento.id
                    detalleSerializador = DocumentoDetalleSerializador(data=detalle)
                    if detalleSerializador.is_valid():
                        documentoDetalle = detalleSerializador.save() 
                        impuestos = detalle.get('impuestos')
                        if impuestos is not None:
                            for impuesto in impuestos:
                                datosDocumentoImpuesto = {
                                    "documento_detalle":documentoDetalle.id, 
                                    "impuesto":impuesto['impuesto'],
                                    "base":impuesto['base'],
                                    "porcentaje":impuesto['porcentaje'],
                                    "total":impuesto['total']
                                }
                                documentoImpuestoSerializador = DocumentoImpuestoSerializador(data=datosDocumentoImpuesto)
                                if documentoImpuestoSerializador.is_valid():
                                    documentoImpuestoSerializador.save()
                                else:
                                    return Response({'mensaje':'Errores de validacion detalle impuesto', 'codigo':14, 'validaciones': documentoImpuestoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                
                    else:
                        return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
                documentoDetalles = DocumentoDetalle.objects.filter(documento=documento.id)
                documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
                detalles = documentoDetallesSerializador.data
                for detalle in detalles:
                    documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
                    documentoImpuestosSerializador = DocumentoImpuestoSerializador(documentoImpuestos, many=True)
                    detalle['impuestos'] = documentoImpuestosSerializador.data
                documentoRespuesta = documentoSerializador.data
                documentoRespuesta['detalles'] = detalles
                return Response({'documento': documentoRespuesta}, status=status.HTTP_200_OK)
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Documento.objects.all()
        documento = get_object_or_404(queryset, pk=pk)
        documentoSerializador = DocumentoSerializador(documento)
        documentoDetalles = DocumentoDetalle.objects.filter(documento=pk)
        documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
        detalles = documentoDetallesSerializador.data
        for detalle in detalles:
            documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
            documentoImpuestosSerializador = DocumentoImpuestoSerializador(documentoImpuestos, many=True)
            detalle['impuestos'] = documentoImpuestosSerializador.data
        documentoRespuesta = documentoSerializador.data
        documentoRespuesta['detalles'] = detalles
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
                        impuestos = detalle.get('impuestos')
                        if impuestos is not None:
                            for impuesto in impuestos:
                                datosDocumentoImpuesto = {
                                    "documento_detalle":documentoDetalle.id, 
                                    "impuesto":impuesto['impuesto'],
                                    "base":impuesto['base'],
                                    "porcentaje":impuesto['porcentaje'],
                                    "total":impuesto['total']
                                }
                                documentoImpuestoSerializador = DocumentoImpuestoSerializador(data=datosDocumentoImpuesto)
                                if documentoImpuestoSerializador.is_valid():
                                    documentoImpuestoSerializador.save()
                                else:
                                    return Response({'mensaje':'Errores de validacion detalle impuesto', 'codigo':14, 'validaciones': documentoImpuestoSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)                                                                        
                        impuestosEliminados = detalle.get('impuestos_eliminados')
                        if impuestosEliminados is not None:
                            for documentoImpuesto in impuestosEliminados:                                
                                documentoImpuesto = DocumentoImpuesto.objects.get(pk=documentoImpuesto)
                                documentoImpuesto.delete()                         
                    else:
                        return Response({'mensaje':'Errores de validacion detalle', 'codigo':14, 'validaciones': detalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)            
            detallesEliminados = raw.get('detalles_eliminados')
            if detallesEliminados is not None:
                for detalle in detallesEliminados:                                
                    documentoDetalle = DocumentoDetalle.objects.get(pk=detalle)
                    documentoDetalle.delete()
            documentoDetalles = DocumentoDetalle.objects.filter(documento=pk)
            documentoDetallesSerializador = DocumentoDetalleSerializador(documentoDetalles, many=True)
            detalles = documentoDetallesSerializador.data
            for detalle in detalles:
                documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle=detalle['id'])
                documentoImpuestosSerializador = DocumentoImpuestoSerializador(documentoImpuestos, many=True)
                detalle['impuestos'] = documentoImpuestosSerializador.data
            documentoRespuesta = documentoSerializador.data
            documentoRespuesta['detalles'] = detalles                   
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
            respuesta = DocumentoViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)     
            return Response(respuesta, status=status.HTTP_200_OK)
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
        respuesta = DocumentoViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)
        
        # Crear un libro de Excel y una hoja
        wb = Workbook()
        ws = wb.active

        # Agregar encabezados de columna
        field_names = [field for field in DocumentoSerializador().get_fields()]
        ws.append(field_names)

        # Agregar datos al archivo Excel
        for row in respuesta['registros']:
            row_data = [row[field] for field in field_names]
            ws.append(row_data)

        # Crear el archivo Excel en memoria
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=documentos.xlsx'
        wb.save(response)
        return response          
    
    @action(detail=False, methods=["post"], url_path=r'imprimir',)
    def imprimir(self, request):
        raw = request.data
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="hello.pdf"'
        p = canvas.Canvas(response)
        p.setFont("Courier", 28)
        p.drawString(0, 0, "Hola mundo")
        p.drawString(60, 750, "Hola mundo")
        p.showPage()
        p.save()
        return response
    
    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        documentos = Documento.objects.all()
        if filtros:
            for filtro in filtros:
                documentos = documentos.filter(**{filtro['propiedad']: filtro['valor_1']})
        if ordenamientos:
            documentos = documentos.order_by(*ordenamientos)              
        documentos = documentos[desplazar:limite+desplazar]
        itemsCantidad = Documento.objects.all()[:limiteTotal].count()
        serializador = DocumentoSerializador(documentos, many=True) 
        campos = []
        camposSerializador = DocumentoSerializador().get_fields()
        for nombre, field_instance in camposSerializador.items():
            tipo = field_instance.__class__.__name__
            etiqueta = field_instance.label or nombre
            campos.append({"nombre": nombre, "tipo": tipo, "etiqueta": etiqueta}) 
          
        respuesta = {'propiedades': campos, 'registros': serializador.data, "cantidad_registros": itemsCantidad}
        return respuesta