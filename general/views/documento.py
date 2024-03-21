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
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
import locale
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from decouple import config
from utilidades.wolframio import consumirPost
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

        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass

        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet['Normal']

        paragraph = Paragraph("El pago se realizará en un plazo de tres meses desde la emisión de esta factura, se realizará mediante transferencia bancaria.", normalStyle)

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
            coord_x = 50
            coord_y = 680
            p.drawImage(logo, coord_x, coord_y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')

            #Emisor
            emisorDireccion = empresa.direccion if empresa.direccion is not None else ""
            p.setFont("Helvetica-Bold", 9)
            p.drawString(150, 720, empresa.nombre_corto.upper() if empresa.nombre_corto else "")
            p.setFont("Helvetica", 8)
            p.drawString(150, 710, "PERSONA " + empresa.tipo_persona.nombre.upper() if empresa.tipo_persona.nombre else "")
            p.drawString(150, 700, "NIT: " + empresa.numero_identificacion + "-" +  empresa.digito_verificacion)
            p.drawString(150, 690, empresa.direccion.upper() + " " +empresa.ciudad.nombre.upper() if empresa.direccion else "")
            p.drawString(150, 680, "TELEFONO " + empresa.telefono if empresa.telefono else "")

            #Datos factura
            p.setFont("Helvetica-Bold", 9)
            p.drawRightString(550, 720, documento.documento_tipo.nombre)
            p.setFont("Helvetica", 9)
            if documento.resolucion:
                if documento.numero:
                    texto_resolucion = documento.resolucion.prefijo + documento.numero
                else:
                    texto_resolucion = documento.resolucion.prefijo
            else:
                texto_resolucion = ""
            p.setFont("Helvetica-Bold", 9)
            p.drawCentredString(470, 710, texto_resolucion)
            p.drawString(390, 690, "FECHA EMISIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 690, str(documento.fecha))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(390, 680, "FECHA VENCIMIENTO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 680, str(documento.fecha_vence))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(390, 670, "FORMA PAGO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 670, str(documento.metodo_pago.nombre.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(390, 660, "PLAZO PAGO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 660, "")

            p.setFont("Helvetica-Bold", 8)
            p.drawString(390, 650, "DOC SOPORTE: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(550, 650, "")


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
            p.drawString(50, 650, "CLIENTE: ")
            p.setFont("Helvetica", 8)
            p.drawString(120, 650, str(clienteNombre))
            
            p.setFont("Helvetica-Bold", 8)
            p.drawString(50, 640, "NIT: ")
            p.setFont("Helvetica", 8)
            p.drawString(120, 640, str(clienteIdentificacion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(50, 630, "DIRECCIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawString(120, 630, str(clienteDireccion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(50, 620, "CIUDAD: ")
            p.setFont("Helvetica", 8)
            p.drawString(120, 620, str(clienteCiudad))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(50, 610, "TELÉFONO: ")
            p.setFont("Helvetica", 8)
            p.drawString(120, 610, str(clienteTelefono))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(50, 600, "CORREO: ")
            p.setFont("Helvetica", 8)
            p.drawString(120, 600, str(clienteCorreo))



            #resolución
            if resolucion:
                texto_resolucion = f"FACTURA ELECTRÓNICA DE VENTA No. {resolucion.prefijo} {documento.numero}"
            else:
                texto_resolucion = f"FACTURA ELECTRÓNICA DE VENTA No. {documento.numero}"
            #p.drawRightString(550, 622, texto_resolucion)
            # p.drawRightString(550, 622, f"FACTURA ELECTRÓNICA DE VENTA No. {resolucion.prefijo} {documento.numero}")
            #Linea separadora
            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(50, 580, 550, 580)
            p.setStrokeColorRGB(0, 0, 0)

            #Encabezado detalles
            p.setFont("Helvetica-Bold", 10)
            p.drawString(60, 555, "Descripción / Producto")
            p.drawString(250, 555, "Impuestos")
            p.drawString(310, 555, "Cantidad")
            p.drawString(380, 555, "Desc")
            p.drawString(440, 555, "Subtotal")
            p.drawString(520, 555, "Total")
            p.setFont("Helvetica", 10)

        def draw_totals(p, y):
            #dejo el llamado de y en caso de que se requiera que se construya de manera dinamica
            #Linea separadora
            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(400, 215, 550, 215)
            p.setStrokeColorRGB(0, 0, 0)

            #Bloque totales
            p.setFont("Helvetica-Bold", 10)
            p.drawString(400, 200, "Subtotal")
            p.drawRightString(550, 200, f"${locale.format_string('%d', int(documento.subtotal), grouping=True)}")
            
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
            y = 180

            # Recorrer el diccionario de totales de impuestos
            for impuesto_id, data in impuesto_totals.items():
                nombre_impuesto = data['nombre']
                total_acumulado = data['total']
                
                p.drawString(400, y, nombre_impuesto)
                p.drawRightString(550, y, f"${locale.format_string('%d', int(total_acumulado), grouping=True)}")
                y -= 20

            p.drawString(400, y, "Total general")
            p.drawRightString(550, y, f"${locale.format_string('%d', int(documento.total), grouping=True)}")

            #Comentario
            paragraph.wrapOn(p, 280, 400)
            paragraph.drawOn(p, 50, 180)

        y = 520
        page_number = 1
        detalles_en_pagina = 0

        draw_header()

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
                itemNombre = detalle.item.nombre[:30]

            p.setStrokeColorRGB(200/255, 200/255, 200/255)
            p.line(50, y + 15, 550, y + 15)
            p.setStrokeColorRGB(0, 0, 0)
            p.drawString(60, y, str(itemNombre))
            p.drawString(250, y, impuestos_str)
            p.drawRightString(350, y, str(int(detalle.cantidad)))
            p.drawRightString(400, y, str(int(detalle.porcentaje_descuento)))
            p.drawRightString(480, y, f"${locale.format_string('%d', int(detalle.subtotal), grouping=True)}")
            p.drawRightString(550, y, f"${locale.format_string('%d', int(detalle.total), grouping=True)}")
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

        p.save()
        return response
    
    @action(detail=False, methods=["post"], url_path=r'emitir',)
    def emitir(self, request):
        try:
            raw = request.data
            codigoDocumento = raw.get('documento_id')
            url = "api/documento/nuevo"
            if codigoDocumento:
                documento = Documento.objects.get(pk=codigoDocumento)
                if documento.estado_aprobado == True:
                    empresa = Empresa.objects.get(pk=1)

                    #Se construye el obejto inicial

                    datos_factura = {
                        "cuentaId": empresa.reddoc_id,
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
                                "ciudad" : documento.contacto.ciudad.codigo_postal,
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
                            "total_impuestos" : str(0),
                            "base" : str(0),
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

                    arr_documento = consumirPost(datos_factura, url)

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
                documentos = documentos.filter(**{filtro['propiedad']: filtro['valor_1']})
        if ordenamientos:
            documentos = documentos.order_by(*ordenamientos)              
        documentos = documentos[desplazar:limite+desplazar]
        itemsCantidad = Documento.objects.all()[:limiteTotal].count()
        serializador = DocumentoSerializador(documentos, many=True)           
        respuesta = {'registros': serializador.data, "cantidad_registros": itemsCantidad}
        return respuesta