from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_impuesto import GenDocumentoImpuesto
from general.models.configuracion import GenConfiguracion
from general.models.empresa import GenEmpresa
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from decouple import config
from django.db.models import Sum
import locale
from django.utils.timezone import localtime
from utilidades.utilidades import Utilidades

class FormatoRemision():

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("factura")
        empresa = GenEmpresa.objects.get(pk=1)
        configuracion = GenConfiguracion.objects.select_related('formato_factura').filter(empresa_id=1).values().first()
        documento = GenDocumento.objects.select_related('empresa', 'documento_tipo', 'contacto', 'contacto__ciudad', 'empresa__tipo_persona',).filter(id=id).values(
        'id', 'fecha', 'fecha_validacion', 'fecha_vence', 'numero', 'soporte', 'contacto_id','subtotal', 'total', 'comentario',
        'contacto__nombre_corto', 'contacto__correo', 'contacto__telefono', 'contacto__numero_identificacion', 'contacto__direccion', 'contacto__ciudad__nombre', 
        'empresa__tipo_persona__nombre', 'empresa__numero_identificacion', 'empresa__digito_verificacion', 'empresa__direccion', 'empresa__telefono',
        'empresa__nombre_corto', 'empresa__imagen', 'empresa__ciudad__nombre', 'documento_tipo__nombre','documento_tipo__documento_clase_id', 'sede__nombre'
        ).first()
        estilo_helvetica = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8, leading=8)
        informacion_factura_superior = configuracion['informacion_factura_superior'] if configuracion['informacion_factura_superior'] else ""
        informacion_factura_superior_con_saltos = informacion_factura_superior.replace('\n', '<br/>')
        informacion_superior = Paragraph(informacion_factura_superior_con_saltos, estilo_helvetica)
        comentario = Paragraph("<b>COMENTARIOS: </b>" +  str(documento['comentario'] if documento['comentario'] else  ""), estilo_helvetica)

        try:
            locale.setlocale(locale.LC_ALL, 'es_CO.utf8')
        except locale.Error:
            pass


        def draw_header():

            region = config('DO_REGION')
            bucket = config('DO_BUCKET')

            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{empresa.imagen}'
            try:
                logo = ImageReader(logo_url)

                p.drawImage(logo, 20, y - 40, width=tamano_cuadrado + 40, height=tamano_cuadrado + 40, mask='auto', preserveAspectRatio=True)

            except Exception as e:
                pass

            x = 24
            ancho_texto, alto_texto = informacion_superior.wrapOn(p, 480, 500)                        
            y2 = 690 - alto_texto
            informacion_superior.drawOn(p, x+76, y2)
            tamano_cuadrado = 1 * inch
            y = 680
            

            #borde tabla detalles
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')
            p.setStrokeColorRGB(0.8, 0.8, 0.8)
            #recuadro1
            p.rect(x, 570, 564, 15)
            #recuadro2
            p.rect(x, 240, 564, 330)


            #Emisor
            numero_identificacion = ""
            if documento['empresa__numero_identificacion']:
                numero_identificacion = numero_identificacion+documento['empresa__numero_identificacion']
            if documento['empresa__digito_verificacion']:
                numero_identificacion = numero_identificacion+"-"+documento['empresa__digito_verificacion']
            direccion = ""
            if documento['empresa__direccion']:
                direccion = direccion+documento['empresa__direccion']
            if documento['empresa__ciudad__nombre']:
                direccion = direccion+" - "+documento['empresa__ciudad__nombre'].upper()
            p.setFont("Helvetica-Bold", 9)
            p.drawString(x + 75, 735, documento['empresa__nombre_corto'].upper() if documento['empresa__nombre_corto'] else "")
            p.setFont("Helvetica", 8)
            p.drawString(x + 75, 725, "NIT: " + numero_identificacion + (" - PERSONA " + documento['empresa__tipo_persona__nombre'].upper() if documento['empresa__tipo_persona__nombre'] else ""))
            p.drawString(x + 75, 715, "DIRECCIÓN: " + direccion)
            p.drawString(x + 75, 705, "TEL: " + documento['empresa__telefono'] if documento['empresa__telefono'] else "")


            #Datos factura
            p.setFont("Helvetica-Bold", 9)
            p.drawRightString(x + 520, 720, documento['documento_tipo__nombre'])
            p.setFont("Helvetica", 9)
            p.setFont("Helvetica", 9)
            texto_resolucion = Utilidades.pdf_texto(documento['numero'])
            p.drawCentredString(x + 500, 710, texto_resolucion)

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 650, "FECHA ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 560, 650, str(documento['fecha']))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 350, 640, "SEDE: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 560, 640, str(documento['sede__nombre']))


            #Cliente
            clienteNombre = ""
            clienteCiudad = ""
            clienteCorreo = ""
            clienteTelefono = ""
            clienteIdentificacion = ""
            clienteDireccion = ""
            if documento['contacto_id'] is not None:
                 clienteNombre = documento['contacto__nombre_corto']
                 clienteCiudad = documento['contacto__ciudad__nombre']
                 clienteCorreo = documento['contacto__correo']
                 clienteTelefono = documento['contacto__telefono']
                 clienteIdentificacion =  documento['contacto__numero_identificacion']
                 clienteDireccion = documento['contacto__direccion']

            
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
            p.drawString(160, 575, "ÍTEM")
            p.drawString(280, 575, "ALM")
            p.drawString(332, 575, "REF")            
            p.drawString(x + 340, 575, "CANT")
            p.drawString(x + 380, 575, "PRECIO")
            p.drawString(x + 430, 575, "DESC")
            p.drawString(x + 470, 575, "IMPUESTO")
            p.drawString(x + 520, 575, "TOTAL")
            p.setFont("Helvetica", 8)

            x = 30

            #comentarios
            ancho_texto, alto_texto = comentario.wrapOn(p, 300, 400)
            
            x = 30
            y = 235 - alto_texto
            y2 = 160
            comentario.drawOn(p, x, y)
        

        # Línea separadora y título ENTREGA (izquierda)
        p.setFont("Helvetica-Bold", 9)
        p.drawString(170, 150, "ENTREGA")

        # Línea separadora y título RECIBE (derecha)
        p.setStrokeColorRGB(0, 0, 0)
        p.drawString(410, 150, "RECIBE")

        # Espacio para firmas - SECCIÓN ENTREGA (izquierda)
        p.setFont("Helvetica", 8)

        # Configuración para líneas uniformes
        left_section_x = 80      # Inicio sección izquierda
        right_section_x = 320     # Inicio sección derecha
        line_length = 150         # Longitud fija para todas las líneas

        # Líneas para firma ENTREGA (izquierda)
        y_position = 120
        campos = ["FIRMA:", "NOMBRE:", "CEDULA:", "CARGO:", "FECHA:"]

        for campo in campos:
            p.drawString(left_section_x, y_position, campo)
            # Dibujar línea más cerca del texto y un poco más abajo
            p.setStrokeColorRGB(0.7, 0.7, 0.7)
            p.setLineWidth(0.3)
            p.line(left_section_x + 45, y_position + 2, left_section_x + 45 + line_length, y_position + 2)
            p.setStrokeColorRGB(0, 0, 0)
            y_position -= 20

        # SECCIÓN RECIBE (derecha) - misma estructura
        y_position = 120
        for campo in campos:
            p.drawString(right_section_x, y_position, campo)
            # Dibujar línea más cerca del texto y un poco más abajo
            p.setStrokeColorRGB(0.7, 0.7, 0.7)
            p.setLineWidth(0.3)
            p.line(right_section_x + 45, y_position + 2, right_section_x + 45 + line_length, y_position + 2)
            p.setStrokeColorRGB(0, 0, 0)
            y_position -= 20

        # Número de página
        p.drawCentredString(550, 20, "Página %d de %d" % (p.getPageNumber(), p.getPageNumber()))

        y = 555

        # Inicialización
        draw_header()
        x = 24
        max_altura_disponible = 330  # Altura máxima disponible en la página para los ítems
        altura_acumulada = 0  # Altura acumulada por los ítems en la página
        y = 550  # Posición vertical inicial
        detalles_en_pagina = 0
        cantidad_total_items = 0

        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento['id']).values('id', 'cantidad', 'precio', 'descuento', 'subtotal', 'impuesto', 'total','item__nombre', 'item_id', 'item__referencia', 'almacen__nombre')
        for index, detalle in enumerate(documento_detalles):

            # Texto del nombre del ítem
            itemNombre = ""
            if detalle['item__nombre'] is not None:
                itemNombre = detalle['item__nombre']
            item_nombre_paragraph = Paragraph(itemNombre, ParagraphStyle(name='ItemNombreStyle', fontName='Helvetica', fontSize=6))  # Reducido a 6
            ancho, alto = item_nombre_paragraph.wrap(180, 100)        
            altura_requerida = alto + 10  # Reducido de 10 a 8
            
            # Verificar si hay suficiente espacio para el siguiente ítem
            if altura_acumulada + altura_requerida > max_altura_disponible:
                p.showPage()
                y = 550  # Restablecer altura disponible para nueva página
                draw_header()
                altura_acumulada = 0
                detalles_en_pagina = 0

            item_nombre_paragraph.drawOn(p, x + 58, y - alto + 5)
            y -= altura_requerida
            altura_acumulada += altura_requerida

            # Referencia como campo separado
            referencia = ""
            if detalle['item__referencia']:
                referencia = str(detalle['item__referencia'])

            almacen = ""
            if detalle['almacen__nombre']:
                almacen = str(detalle['almacen__nombre'])                
            
            p.setFont("Helvetica", 7)
            p.drawString(x + 300, y + alto + 6, f"{referencia[:10]}")
            p.drawString(x + 245, y + alto + 6, f"{almacen[:10]}")
            p.drawCentredString(x + 7, y + alto + 6, str(index + 1))
            p.drawString(x + 25, y + alto + 6, str(detalle['item_id']))
            p.drawRightString(x + 365, y + alto + 6, str(detalle['cantidad']))
            p.drawRightString(x + 417, y + alto + 6, f"{detalle['precio']:,.0f}")
            p.drawRightString(x + 458, y + alto + 6, f"{detalle['descuento']:,.0f}")
            p.drawRightString(x + 505, y + alto + 6, f"{detalle['impuesto']:,.0f}")
            p.drawRightString(x + 555, y + alto + 6, f"{detalle['subtotal']:,.0f}")

            y -= 8  # Reducido de 10 a 8
            altura_acumulada += 8
            detalles_en_pagina += 1
            cantidad_total_items += 1

        p.drawString(x + 5, y, "CANTIDAD DE ÍTEMS: " + str(cantidad_total_items))
        x = 440
        totalFactura = documento['total']        
        p.setFont("Helvetica-Bold", 8)
        p.drawString(x, 230, "SUBTOTAL")
        p.drawRightString(x + 140, 230,  f"{documento['subtotal']:,.0f}")

        documento_impuestos = GenDocumentoImpuesto.objects.filter(
            documento_detalle__documento_id=documento['id']
        ).values(
            'impuesto_id', 'impuesto__nombre_extendido'
        ).annotate(
            total_operado=Sum('total_operado')
        ).order_by('impuesto_id')

        y = 220
        for impuesto in documento_impuestos:
            nombre_impuesto = impuesto['impuesto__nombre_extendido']
            total_acumulado = impuesto['total_operado']            
            p.drawString(x, y, nombre_impuesto.upper())
            p.drawRightString(x + 140, y, f"{total_acumulado:,.0f}")
            y -= 10

        p.drawString(x, y, "TOTAL GENERAL")
        p.drawRightString(x + 140, y, f"{totalFactura:,.0f}")

        p.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
