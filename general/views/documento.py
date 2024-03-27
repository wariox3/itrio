from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.models.documento_impuesto import DocumentoImpuesto
from general.models.empresa import Empresa
from general.models.resolucion import Resolucion
from general.serializers.documento import DocumentoSerializador, DocumentoRetrieveSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializador
from openpyxl import Workbook
import locale
from decouple import config
from utilidades.wolframio import consumirPost
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
import json

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
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass

        try:
            documento = Documento.objects.get(pk=codigoDocumento)
            contacto = documento.contacto
            documentoDetalles = DocumentoDetalle.objects.filter(documento_id=codigoDocumento)
            empresa = Empresa.objects.get(pk=documento.empresa.id)
            documentoImpuestos = DocumentoImpuesto.objects.filter(documento_detalle__in=documentoDetalles)
            resolucion = None
            if documento.resolucion_id is not None:
                resolucion = Resolucion.objects.get(pk=documento.resolucion.id)
        except Documento.DoesNotExist:
            pass

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="hello.pdf"'
        p = canvas.Canvas(response, pagesize=letter)


        estilo_helvetica = ParagraphStyle(
        name='HelveticaStyle',
        fontName='Helvetica',
        fontSize=8,
        )

        # Crear los Paragraph con los estilos correspondientes
        informacion_pago_texto = "INFORMACIÓN DE PAGO: "
        comentario_texto = "COMENTARIOS:   "

        # Para el texto del comentario, mantenlo en estilo normal
        comentario_contenido = str(documento.comentario)

        # Crear los Paragraph con los estilos correspondientes
        informacionPago = Paragraph("<b>" + informacion_pago_texto + "</b>", estilo_helvetica)
        comentario = Paragraph("<b>" + comentario_texto + "</b>" + comentario_contenido, estilo_helvetica)

        qr = ""
        if documento.qr:
            qr = documento.qr
        qr_code_drawing = generar_qr(qr)

        # Dibujar el código QR en el lienzo en la posición deseada
        x_pos = 340
        y_pos = 125
        renderPDF.draw(qr_code_drawing, p, x_pos, y_pos)

        def draw_header():

            region = config('DO_REGION')
            bucket = config('DO_BUCKET')
            entorno = config('ENV')

            imagen_defecto_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'

            # Intenta cargar la imagen desde la URL

            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{empresa.imagen}'
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                # Si se produce un error, establece la URL en la imagen de defecto
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

            tamano_cuadrado = 1 * inch
            x = 35
            y = 680

            #borde tabla detalles
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')
            p.setStrokeColorRGB(0.8, 0.8, 0.8)
            #recuadro1
            p.rect(x, 570, 542, 15)
            #recuadro2
            p.rect(x, 240, 542, 330)


            #Emisor
            p.setFont("Helvetica-Bold", 9)
            p.drawString(x + 75, 720, empresa.nombre_corto.upper() if empresa.nombre_corto else "")
            p.setFont("Helvetica", 8)
            p.drawString(x + 75, 710, "PERSONA " + empresa.tipo_persona.nombre.upper() if empresa.tipo_persona.nombre else "")
            p.drawString(x + 75, 700, "NIT: " + empresa.numero_identificacion + "-" +  empresa.digito_verificacion)
            p.drawString(x + 75, 690, empresa.direccion.upper() + " " +empresa.ciudad.nombre.upper() if empresa.direccion else "")
            p.drawString(x + 75, 680, "TEL: " + empresa.telefono if empresa.telefono else "")

            #Datos factura
            p.setFont("Helvetica-Bold", 9)
            p.drawRightString(x + 540, 720, documento.documento_tipo.nombre)
            p.setFont("Helvetica", 9)
            if documento.resolucion:
                if documento.numero:
                    texto_resolucion = documento.resolucion.prefijo + str(documento.numero)
                else:
                    texto_resolucion = documento.resolucion.prefijo
            else:
                texto_resolucion = ""
            p.setFont("Helvetica-Bold", 9)
            p.drawCentredString(x + 460, 710, texto_resolucion)
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 660, "FECHA EMISIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 660, str(documento.fecha))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 650, "FECHA VENCIMIENTO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 650, str(documento.fecha_vence))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 640, "FORMA PAGO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 640, str(documento.metodo_pago.nombre.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 630, "PLAZO PAGO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 630, "")

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 620, "DOC SOPORTE: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 540, 620, "")


            #Cliente
            clienteNombre = ""
            clienteCiudad = ""
            clienteCorreo = ""
            clienteTelefono = ""
            clienteIdentificacion = ""
            clienteDireccion = ""
            if contacto is not None:
                 clienteNombre = contacto.nombre_corto
                 clienteCiudad = contacto.ciudad.nombre
                 clienteCorreo = contacto.correo
                 clienteTelefono = contacto.telefono
                 clienteIdentificacion =  contacto.numero_identificacion
                 clienteDireccion = contacto.direccion

            
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 650, "CLIENTE: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 650, str(clienteNombre))
            
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 640, "NIT: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 640, str(clienteIdentificacion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 630, "DIRECCIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 630, str(clienteDireccion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 620, "CIUDAD: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 620, str(clienteCiudad))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 610, "TELÉFONO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 610, str(clienteTelefono))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 600, "CORREO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 60, 600, str(clienteCorreo))

            #Encabezado detalles
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 5, 575, "#")
            p.drawString(x + 30, 575, "COD")
            p.drawString(200, 575, "ITEM")
            p.drawString(x + 320, 575, "CANT")
            p.drawString(x + 360, 575, "PRECIO")
            p.drawString(x + 410, 575, "DESC")
            p.drawString(x + 450, 575, "IVA")
            p.drawString(x + 490, 575, "TOTAL")
            p.setFont("Helvetica", 8)

        def draw_totals(p, y):

            x = 430

            #Bloque totales
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 230, "SUTOTAL")
            p.drawRightString(x + 140, 230, f"$ {locale.format('%d', documento.subtotal, grouping=True)}")
            
            # Crear un diccionario para almacenar los totales por impuesto_id y su nombre
            impuesto_totals = {}

            # Recorrer los objetos DocumentoImpuesto
            for impuesto in documentoImpuestos:
                impuesto_id = impuesto.impuesto.id  # ID del impuesto
                nombre_impuesto = impuesto.impuesto.nombre_extendido  # Nombre del impuesto
                total = impuesto.total

                # Verificar si el impuesto_id ya existe en el diccionario
                if impuesto_id in impuesto_totals:
                    # Si existe, sumar el total al valor existente
                    impuesto_totals[impuesto_id]['total'] += total
                else:
                    # Si no existe, crear una nueva entrada en el diccionario con el total y el nombre del impuesto
                    impuesto_totals[impuesto_id] = {'total': total, 'nombre': nombre_impuesto}

            # Definir la posición "y" inicial
            y = 220

            # Recorrer el diccionario de totales de impuestos
            for impuesto_id, data in impuesto_totals.items():
                nombre_impuesto = data['nombre']
                total_acumulado = data['total']
                
                p.drawString(x, y, nombre_impuesto.upper())
                p.drawRightString(x + 140, y, f"$ {locale.format('%d', total_acumulado, grouping=True)}")
                y -= 10

            p.drawString(x, y, "TOTAL GENERAL")
            p.drawRightString(x + 140, y, f"$ {locale.format('%d', documento.total, grouping=True)}")

            #informacion pago
            ancho_texto, alto_texto = informacionPago.wrapOn(p, 280, 380)
            
            #comentarios
            ancho_texto, alto_texto = comentario.wrapOn(p, 300, 400)
            
            x = 38
            y = 235 - alto_texto
            y2 = 160
            comentario.drawOn(p, x, y)
            informacionPago.drawOn(p, x, y2)
            
        y = 555
        page_number = 1
        detalles_en_pagina = 0

        draw_header()
        x = 35

        for index, detalle in enumerate(documentoDetalles):
            impuestos_detalle = documentoImpuestos.filter(documento_detalle_id=detalle.id)
            impuestos_unicos = []
            # Iterar sobre los impuestos relacionados con el detalle actual
            for impuesto_detalle in impuestos_detalle:
                nombre_impuesto = impuesto_detalle.impuesto.nombre
                
                # Si el nombre del impuesto no está en la lista de impuestos únicos, agrégalo
                if nombre_impuesto not in impuestos_unicos:
                    impuestos_unicos.append(nombre_impuesto)

                # Ahora, puedes imprimir los nombres de impuestos únicos en una línea
                impuestos_str = ', '.join(impuestos_unicos)
            itemNombre = ""
            if detalle.item is not None:
                itemNombre = detalle.item.nombre[:100]

            p.drawCentredString(x + 7, y, str(index + 1))
            p.drawString(x + 25, y, detalle.item.codigo)
            p.drawString(100, y, str(itemNombre[:57]))
            p.drawRightString(x + 345, y, str(int(detalle.cantidad)))
            p.drawRightString(x + 395, y, locale.format_string("%d", detalle.precio, grouping=True))
            p.drawRightString(x + 440, y, locale.format_string("%d", detalle.descuento, grouping=True))
            p.drawRightString(x + 470, y, locale.format_string("%d", 0, grouping=True))
            p.drawRightString(x + 530, y, locale.format_string("%d", detalle.total, grouping=True))
            #p.drawString(250, y, impuestos_str)
            #p.drawRightString(400, y, str(int(detalle.porcentaje_descuento)))
            #p.drawRightString(480, y, f"${locale.format_string('%d', int(detalle.subtotal), grouping=True)}")
            #p.drawRightString(550, y, f"${locale.format_string('%d', int(detalle.total), grouping=True)}")
            y -= 30
            detalles_en_pagina += 1

            if detalles_en_pagina == 10 or index == len(documentoDetalles) - 1:
                draw_totals(p, y)

                if index != len(documentoDetalles) - 1:
                    p.showPage()
                    page_number += 1
                    y = 520
                    draw_header()
                    detalles_en_pagina = 0

        p.drawString(x + 5, y, "CANTIDAD DE ITEMS: " + str(detalles_en_pagina))
        def draw_footer(pageCount):
            x = 35

            valorLetras = convertir_a_letras(int(documento.total))

            consecutivoDesde = ""
            consecutivoHasta = ""
            numero = ""
            fechaVigencia = ""
            if resolucion:
                consecutivoDesde = documento.resolucion.consecutivo_desde
                consecutivoHasta = documento.resolucion.consecutivo_hasta
                numero = documento.resolucion.numero
                fechaVigencia = documento.resolucion.fecha_hasta

            cue = ""
            if documento.cue:
                cue = documento.cue

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 120, str(valorLetras))

            p.drawString(x, 110, "CUFE/CUDE: ")
            p.setFont("Helvetica", 8)
            p.drawString(105, 110, str(cue))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 100, "NUMERO DE AUTORIZACIÓN:")
            p.setFont("Helvetica", 8)
            p.drawString(170, 100, str(numero))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(250, 100, "RANGO AUTORIZADO DESDE: ")
            p.setFont("Helvetica", 8)
            p.drawString(370, 100, str(consecutivoDesde))
            p.setFont("Helvetica-Bold", 8)
            p.drawString(400, 100, "HASTA: ")
            p.setFont("Helvetica", 8)
            p.drawString(432, 100, str(consecutivoHasta))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(465, 100, "VIGENCIA: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 100, str(fechaVigencia))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 90, "GENERADO POR: ")
            p.setFont("Helvetica", 8)
            p.drawString(110, 90, "REDDOC")

            p.setFont("Helvetica-Bold", 8)
            p.drawString(250, 90, "PROVEEDOR TECNOLOGICO: ")
            p.setFont("Helvetica", 8)
            p.drawString(370, 90, "SOFTGIC S.A.S")

            p.setStrokeColorRGB(0.8, 0.8, 0.8)
            p.setLineWidth(0.5)
            p.line(50, 45, 250, 45)
            p.setStrokeColorRGB(0, 0, 0)
            p.setFont("Helvetica-Bold", 8)
            p.drawCentredString(150, 30, "ELABORADO POR")

            p.setStrokeColorRGB(0.8, 0.8, 0.8)  # Color tenue (gris claro)
            p.setLineWidth(0.5)  # Grosor de la línea
            p.line(270, 45, 550, 45)  # Coordenadas para dibujar la segunda línea
            p.setStrokeColorRGB(0, 0, 0)  # Restaurar el color a negro
            p.drawCentredString(410, 30, "ACEPTADA, FIRMADA Y/O SELLO Y FECHA")
    
            # Dibuja el número de página centrado
            p.drawCentredString(550, 20, "Página %d de %d" % (p.getPageNumber(), pageCount))

        total_pages = p.getPageNumber()

        draw_footer(total_pages)

        p.save()
        return response
    
    @action(detail=False, methods=["post"], url_path=r'emitir',)
    def emitir(self, request):
        try:
            raw = request.data
            codigoDocumento = raw.get('documento_id')
            url = "/api/documento/nuevo"
            if codigoDocumento:
                documento = Documento.objects.get(pk=codigoDocumento)
                if documento.estado_aprobado == True:
                    empresa = Empresa.objects.get(pk=1)

                    #Se construye el obejto inicial

                    datos_factura = {
                        "cuentaId": empresa.rededoc_id,
                        "documentoClaseId" : 1,
                        "documento" : {
                            "ambiente" : documento.resolucion.ambiente,
                            "prefijo" : documento.resolucion.prefijo,
                            "numero" : documento.numero,
                            "fecha" : str(documento.fecha),
                            "hora" : str("12:00:00-05:00"),
                            "fecha_vence" : str(documento.fecha_vence),
                            "tipo_operacion" : str(10),
                            "moneda" : "COP",
                            "resolucion" : documento.resolucion.numero,
                            "forma_pago" : documento.metodo_pago.id,
                            "cantidad_detalles" :1,
                            "subtotal" : str(documento.subtotal),
                            "subtotal_mas_impuestos" : str(documento.subtotal + documento.impuesto),
                            "base" : str(documento.base_impuesto),
                            "total_impuestos" : str(documento.impuesto),
                            "total_descuentos" : str(documento.descuento),
                            "total_cargos" : str(0),
                            "total_anticipos" : str(0),
                            "total_documento" : str(documento.total),
                            "total_iva" : str(0),
                            "total_consumo" : str(0),
                            "total_ica" : str(0),
                            "adquiriente" : {
                                "identificacion" : documento.contacto.identificacion.codigo,
                                "numero_identificacion" : documento.contacto.numero_identificacion,
                                "digito_verificacion" : documento.contacto.digito_verificacion,
                                "razon_social" : documento.contacto.nombre_corto,
                                "pais" : "CO",
                                "ciudad" : documento.contacto.ciudad.nombre,
                                "departamento" : documento.contacto.ciudad.estado.nombre,
                                "direccion" : documento.contacto.direccion,
                                "obligaciones" : "0-99",
                                "nombres" : documento.contacto.nombre1,
                                "apellidos" : documento.contacto.apellido1,
                                "correo" : documento.contacto.correo,
                                "telefono" : documento.contacto.telefono,
                                "tipo_organizacion_juridica" : documento.contacto.tipo_persona.id,
                                "regimen_tributario" : documento.contacto.regimen.id,
                                "codigo_postal" : documento.contacto.ciudad.codigo_postal,
                                "responsable" : 1,
                                "nacional" : 1
                            },
                        }
                    }
                    arr_medio_pago = []

                    arr_medio_pago.append({
                        "medio_pago": 31,
                        "descripcion": "",
                    })

                    datos_factura['documento']['medios_pago'] = arr_medio_pago

                    arr_item = []
                    cantidad_items = 0
                    impuestos_agrupados = {}

                    documentoDetalles = DocumentoDetalle.objects.filter(documento=codigoDocumento)
                    for documentoDetalle in documentoDetalles:
                        arr_impuestos = []
                        documentoImpuestoDetalles = DocumentoImpuesto.objects.filter(documento_detalle=documentoDetalle.id)
                        for documentoImpuestoDetalle in documentoImpuestoDetalles:
                            impuesto_id = documentoImpuestoDetalle.impuesto_id
                            total = documentoImpuestoDetalle.total
                            arr_impuestos.append({
                                "tipo_impuesto" : documentoImpuestoDetalle.impuesto_id,
                                "total" : str(documentoImpuestoDetalle.total),
                                "porcentual" : str(documentoImpuestoDetalle.porcentaje)
                            })

                            if impuesto_id in impuestos_agrupados:
                                impuestos_agrupados[impuesto_id] += total
                            else:
                                impuestos_agrupados[impuesto_id] = total

                        cantidad_items += 1
                        arr_item.append({
                            "consecutivo": cantidad_items,
                            "codigo": documentoDetalle.item.codigo,
                            "descripcion" : documentoDetalle.item.nombre,
                            "marca" : "",
                            "modelo" : "",
                            "observacion" : "",
                            "cantidad" : str(documentoDetalle.cantidad),
                            "cantidad_empque": str(documentoDetalle.cantidad),
                            "obserquio" : str(0),
                            "precio_unitario" : str(documentoDetalle.precio),
                            "precio_referencia" : str(documentoDetalle.precio),
                            "valor" : str(documentoDetalle.precio),
                            "total_descuentos" : str(documentoDetalle.descuento),
                            "total_cargos" : str(0),
                            "total_impuestos" : str(documentoImpuestoDetalle.total),
                            "base" : str(documentoImpuestoDetalle.base),
                            "subtotal" : str(documentoDetalle.subtotal),
                            "impuestos" : arr_impuestos
                        })

                    arr_impuestos = []
                    for impuesto_id, total in impuestos_agrupados.items():
                        arr_impuestos.append({
                            "tipo_impuesto": impuesto_id,
                            "total": str(total),
                            "porcentual" : str(19.00)
                        })
                    
                    datos_factura['documento']['detalles'] = arr_item
                    datos_factura['doc_cantidad_item'] = cantidad_items
                    datos_factura['documento']['impuestos'] = arr_impuestos

                    respuesta = consumirPost(datos_factura, url)

                    if 'id' in respuesta:
                        return Response({'emitir': True, 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje': {respuesta.get('mensaje')}, 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje': 'El documento no se puede emitir ya que no está aprobado', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        except Documento.DoesNotExist:
            return Response({'mensaje': 'El documento no existe', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        documentos = Documento.objects.all()
        if filtros:
            for filtro in filtros:
                documentos = documentos.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            documentos = documentos.order_by(*ordenamientos)              
        documentos = documentos[desplazar:limite+desplazar]
        itemsCantidad = Documento.objects.all()[:limiteTotal].count()
        serializador = DocumentoSerializador(documentos, many=True)           
        respuesta = {'registros': serializador.data, "cantidad_registros": itemsCantidad}
        return respuesta