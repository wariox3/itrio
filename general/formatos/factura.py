from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF

class FormatoFactura():

    def generar_pdf(self, data):  
        buffer = BytesIO()                              
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        estilo_helvetica = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8)
        informacionPago = Paragraph("<b>INFORMACIÓN DE PAGO: </b>", estilo_helvetica)
        comentario = Paragraph("<b>COMENTARIOS: </b>", estilo_helvetica)

        '''
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
        '''

        elements = []
        elements.append(Paragraph("Hola mundo", estilo_helvetica))
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
