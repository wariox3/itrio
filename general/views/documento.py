from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.models.documento_impuesto import DocumentoImpuesto
from general.serializers.documento import DocumentoSerializador, DocumentoRetrieveSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializador
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
import locale

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
        documentoSerializador = DocumentoRetrieveSerializador(documento)
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
                        documentoDetalle = detalleSerializador.save() 
                        impuestos = detalle.get('impuestos')
                        if impuestos is not None:
                            for impuesto in impuestos:
                                if impuesto.get('id'):
                                    documentoImpuesto = DocumentoImpuesto.objects.get(pk=impuesto['id'])
                                    documentoImpuestoSerializador = DocumentoImpuestoSerializador(documentoImpuesto, data=impuesto, partial=True)    
                                else:        
                                    impuesto['documento_detalle'] = documentoDetalle.id                                     
                                    documentoImpuestoSerializador = DocumentoImpuestoSerializador(data=impuesto)                            
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
        codigoDocumento = raw.get('documento_id')

        try:
            documento = Documento.objects.get(pk=codigoDocumento)
            contacto = documento.contacto
            documentoDetalles = DocumentoDetalle.objects.filter(documento_id=codigoDocumento)
        except Documento.DoesNotExist:
            pass

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="hello.pdf"'
        p = canvas.Canvas(response, pagesize=letter)

        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass

        def draw_header():
            p.setFont("Helvetica", 10)
            p.drawString(270, 740, "Razón social")
            p.drawString(270, 726, "Identificación - NIT")
            p.drawString(270, 712, "Dirección")
            p.drawString(270, 698, "Teléfono - celular")

            p.setFont("Helvetica-Bold", 11.5)
            p.drawRightString(550, 690, f"FACTURA N°: {documento.numero}")
            p.setFont("Helvetica", 10)
            p.drawRightString(550, 676, f"Fecha: {documento.fecha}")

            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, 670, "Datos cliente")
            p.setFont("Helvetica", 10)
            nombre_corto = getattr(contacto, 'nombre_corto', 'Vacio' if not contacto else '')
            p.drawString(50, 650, str(nombre_corto))
            p.drawString(50, 636, str(contacto.direccion))
            p.drawString(50, 622, str(contacto.ciudad.nombre))
            p.drawString(50, 608, str(contacto.correo))
            p.drawString(50, 594, str(contacto.telefono))

            # Línea separadora
            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(50, 580, 550, 580)
            p.setStrokeColorRGB(0, 0, 0)

            # Encabezado de la tabla de productos
            p.setFont("Helvetica-Bold", 10)
            p.drawString(60, 555, "Descripción / Producto")
            p.drawString(310, 555, "Cantidad")
            p.drawString(380, 555, "Desc")
            p.drawString(440, 555, "Subtotal")
            p.drawString(520, 555, "Total")
            p.setFont("Helvetica", 10)

        def draw_totals(p, total, y):
            p.setFont("Helvetica", 10)
            p.drawString(50, y - 20, "Subtotal:")
            p.drawString(50, y - 20, f"${total:.2f}")
            p.drawString(450, y - 20, locale.currency(total, grouping=True))

        y = 520
        page_number = 1
        detalles_en_pagina = 0

        draw_header()

        for index, detalle in enumerate(documentoDetalles):
            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(50, y + 15, 550, y + 15)
            p.setStrokeColorRGB(0, 0, 0)
            p.drawString(70, y, str(detalle.item.nombre[:30]))
            p.drawRightString(350, y, str(int(detalle.cantidad)))
            p.drawRightString(400, y, str(int(detalle.porcentaje_descuento)))
            p.drawRightString(480, y, f"${locale.format_string('%d', int(detalle.subtotal), grouping=True)}")
            p.drawRightString(550, y, f"${locale.format_string('%d', int(detalle.total), grouping=True)}")
            y -= 30
            detalles_en_pagina += 1

            if detalles_en_pagina == 10 or index == len(documentoDetalles) - 1:
                total = sum(det.subtotal for det in documentoDetalles[:index+1])
                if detalles_en_pagina < 10 and index != len(documentoDetalles) - 1:
                    # Si no hay 10 detalles en la página y no es la última página, muestra los totales
                    draw_totals(p, total, y)

                if index != len(documentoDetalles) - 1:
                    # Si no es la última página, crea una nueva página
                    p.showPage()
                    page_number += 1
                    y = 520
                    draw_header()
                    detalles_en_pagina = 0

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
    
    def emitir():
        return []