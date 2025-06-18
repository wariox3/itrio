from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from io import BytesIO
from utilidades.utilidades import generar_qr
from reportlab.graphics import renderPDF
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_impuesto import GenDocumentoImpuesto
from datetime import datetime
from collections import defaultdict, OrderedDict

class FormatoFacturaPOS():
    
    def __init__(self):
        # Configuración de estilos
        self.estilo_normal = ParagraphStyle(
            name='Normal',
            fontName='Courier',
            fontSize=7,
            leading=7,
            spaceAfter=2,
            leftIndent=0,
            rightIndent=0,
            wordWrap=True
        )
        
        self.estilo_negrita = ParagraphStyle(
            name='Negrita',
            fontName='Courier-Bold',
            fontSize=7,
            leading=7,
            spaceAfter=2,
            leftIndent=0,
            rightIndent=0,
            wordWrap=True
        )
        
        self.estilo_derecha = ParagraphStyle(
            name='Derecha',
            fontName='Courier',
            fontSize=7,
            leading=6,
            alignment=2
        )

    def generar_pdf(self, id):
        # Configuración básica
        ANCHO = 80 * mm
        MARGEN = 5 * mm
        buffer = BytesIO()
        
        # Obtener datos del documento
        documento = self.obtener_datos_documento(id)
        
        # Calcular altura total requerida
        altura_total = self.calcular_altura_total(documento)
        
        # Crear canvas con altura dinámica
        p = canvas.Canvas(buffer, pagesize=(ANCHO, altura_total))
        p.setTitle("Factura POS")

        y = altura_total - MARGEN
        y = self.dibujar_encabezado(p, documento, ANCHO, y, MARGEN)
        y = self.dibujar_datos_cliente(p, documento, y, MARGEN)
        y = self.dibujar_linea_divisoria(p, y, ANCHO, MARGEN)
        y = self.dibujar_detalles_productos(p, documento, y, MARGEN)
        y = self.dibujar_totales(p, documento, y, MARGEN)
        y = self.dibujar_desglose_impuestos(p, documento, y, MARGEN)
        y = self.dibujar_resolucion(p, documento, y, MARGEN)
        y = self.dibujar_datos_electronicos(p, documento, y, ANCHO, MARGEN)
        p.showPage()
        p.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def obtener_datos_documento(self, id):
        """Obtiene todos los datos necesarios del documento en una sola consulta"""
        documento = GenDocumento.objects.select_related(
            'empresa', 'documento_tipo', 'contacto', 'resolucion', 
            'metodo_pago', 'contacto__ciudad', 'empresa__tipo_persona', 
            'documento_referencia', 'plazo_pago'
        ).filter(id=id).first()
        
        # Obtener detalles e impuestos
        detalles = GenDocumentoDetalle.objects.filter(documento_id=id)
        impuestos = GenDocumentoImpuesto.objects.filter(
            documento_detalle__documento_id=id
        ).select_related('impuesto')
        
        # Organizar impuestos por detalle
        impuestos_por_detalle = defaultdict(list)
        for imp in impuestos:
            if imp.impuesto.nombre:
                impuestos_por_detalle[imp.documento_detalle_id].append(imp.impuesto.nombre)
        
        return {
            'documento': documento,
            'detalles': detalles,
            'impuestos_por_detalle': impuestos_por_detalle,
            'impuestos': impuestos
        }

    def calcular_altura_total(self, data):
        """Calcula la altura total necesaria para el PDF"""
        doc = data['documento']
        altura = 10 * mm
        
        altura += 4 * 4 * mm
        altura += 6 * 4 * mm
        altura += 8 * mm 
        for detalle in data['detalles']:
            item_paragraph = Paragraph(detalle.item.nombre, self.estilo_normal)
            item_paragraph.wrapOn(None, 40 * mm, 20 * mm)
            altura += max(item_paragraph.height, 7 * mm) + 1 * mm
        
        altura += 7 * 4 * mm
        
        altura += 4 * mm
        altura += len(data['impuestos']) * 4 * mm 
        
        if doc.resolucion:
            altura += 2 * 4 * mm
        
        if doc.cue:
            cue_paragraph = Paragraph(f"Cufe: {doc.cue}", self.estilo_normal)
            cue_paragraph.wrapOn(None, 60 * mm, 20 * mm)
            altura += cue_paragraph.height + 12 * mm
        
        if doc.qr:
            altura += 24 * mm
            
        return altura + 10 * mm

    def dibujar_encabezado(self, p, data, ancho, y, margen):
        doc = data['documento']
        centro_pagina = ancho / 2
        

        nit = f"{doc.empresa.numero_identificacion or ''}"
        if doc.empresa.digito_verificacion:
            nit += f"-{doc.empresa.digito_verificacion}"
            
        direccion = f"{doc.empresa.direccion or ''}"
        if doc.empresa.ciudad:
            direccion += f" - {doc.empresa.ciudad.nombre.upper()}"
        

        p.setFont("Courier-Bold", 8)
        nombre = doc.empresa.nombre_corto.upper() if doc.empresa.nombre_corto else ""
        ancho_texto = p.stringWidth(nombre, "Courier-Bold", 8)
        p.drawString(centro_pagina - (ancho_texto/2), y, nombre)
        y -= 4 * mm
        
        p.setFont("Courier", 7)
        nit_texto = f"NIT: {nit}"
        ancho_texto = p.stringWidth(nit_texto, "Courier", 7)
        p.drawString(centro_pagina - (ancho_texto/2), y, nit_texto)
        y -= 4 * mm

        y = self.dibujar_texto_centrado(p, direccion, centro_pagina, y, tamano=7)
        y -= 4 * mm
        
        tel_texto = f"Tel: {doc.empresa.telefono}"
        ancho_texto = p.stringWidth(tel_texto, "Courier", 7)
        p.drawString(centro_pagina - (ancho_texto/2), y, tel_texto)
        
        return y - 5 * mm


    def dibujar_datos_cliente(self, p, data, y, margen):
        doc = data['documento']
        fecha = doc.fecha.strftime('%Y/%m/%d')
        
        y = self.dibujar_texto_izquierda(p, f"Número: {doc.numero or ''}", margen, y)
        y = self.dibujar_texto_izquierda(p, f"Fecha: {fecha}", margen, y)
        y = self.dibujar_texto_izquierda(p, f"Cliente: {doc.contacto.nombre_corto}", margen, y)
        y = self.dibujar_texto_izquierda(p, f"Nit/C.C: {doc.contacto.numero_identificacion}", margen, y)
        y = self.dibujar_texto_izquierda(p, f"Dirección: {doc.contacto.direccion}", margen, y)
        y = self.dibujar_texto_izquierda(p, f"Teléfono: {doc.contacto.telefono}", margen, y)
        
        return y

    def dibujar_detalles_productos(self, p, data, y, margen):
        # Encabezado tabla
        p.setFont("Courier-Bold", 7)
        p.drawString(margen, y, "Ítem")
        p.drawString(margen + 40 * mm, y, "Cant")
        p.drawString(margen + 55 * mm, y, "Subtotal")
        y -= 8 * mm
        
        # Detalles
        for detalle in data['detalles']:
            nombre = detalle.item.nombre
            impuestos = data['impuestos_por_detalle'].get(detalle.id, [])
            
            if impuestos:
                nombre += f" ({', '.join(impuestos)})"
            
            # Dibujar nombre del producto
            item_para = Paragraph(nombre, self.estilo_normal)
            item_para.wrapOn(p, 40 * mm, 20 * mm)
            item_para.drawOn(p, margen, y - item_para.height + 4 * mm)
            
            # Dibujar cantidad
            cant_para = Paragraph(str(detalle.cantidad), self.estilo_derecha)
            cant_para.wrapOn(p, 10 * mm, 20 * mm)
            cant_para.drawOn(p, margen + 40 * mm, y - cant_para.height + 4 * mm)
            
            # Dibujar subtotal
            subtotal_para = Paragraph(f"{detalle.subtotal:,.0f}", self.estilo_derecha)
            subtotal_para.wrapOn(p, 20 * mm, 20 * mm)
            subtotal_para.drawOn(p, margen + 50 * mm, y - subtotal_para.height + 4 * mm)
            
            y -= max(item_para.height, cant_para.height, subtotal_para.height) + 1 * mm
        
        return y

    def dibujar_totales(self, p, data, y, margen):
        doc = data['documento']
        
        y = self.dibujar_linea_divisoria(p, y, 80 * mm, margen)
        
        p.setFont("Courier-Bold", 7)
        p.drawString(margen, y, "Total:")
        p.drawRightString(margen + 70 * mm, y, f"{doc.total:,.0f}")
        y -= 4 * mm
        
        p.drawString(margen, y, "Total items:")
        p.drawRightString(margen + 70 * mm, y, str(data['detalles'].count()))
        y -= 4 * mm
        
        y = self.dibujar_linea_divisoria(p, y, 80 * mm, margen)
        
        p.drawString(margen, y, "Vta antes de impuestos:")
        p.drawRightString(margen + 70 * mm, y, f"{doc.subtotal:,.0f}")
        y -= 4 * mm
        
        p.drawString(margen, y, "Impuestos:")
        p.drawRightString(margen + 70 * mm, y, f"{doc.impuesto:,.0f}")
        y -= 4 * mm
        
        return y

    def dibujar_desglose_impuestos(self, p, data, y, margen):
        doc = data['documento']
        
        y = self.dibujar_linea_divisoria(p, y, 80 * mm, margen)
        
        p.setFont("Courier-Bold", 7)
        p.drawString(margen, y, "Descripción")
        p.drawString(margen + 36 * mm, y, "Vr base")
        p.drawString(margen + 55 * mm, y, "Vr impto")
        y -= 4 * mm
        
        p.setFont("Courier", 7)
        
        # Agrupar impuestos por nombre
        impuestos_agrupados = defaultdict(lambda: {'base': 0, 'total': 0})
        for imp in data['impuestos']:
            nombre = imp.impuesto.nombre_extendido
            impuestos_agrupados[nombre]['base'] += imp.base
            impuestos_agrupados[nombre]['total'] += imp.total_operado
        
        # Dibujar impuestos
        for nombre, valores in impuestos_agrupados.items():
            p.drawString(margen, y, nombre)
            p.drawRightString(margen + 50 * mm, y, f"{valores['base']:,.0f}")
            p.drawRightString(margen + 70 * mm, y, f"{valores['total']:,.0f}")
            y -= 4 * mm
        
        return y

    def dibujar_resolucion(self, p, data, y, margen):
        doc = data['documento']
        
        if doc.resolucion:
            y = self.dibujar_linea_divisoria(p, y, 80 * mm, margen)
            y -= 4 * mm
            
            y = self.dibujar_texto_izquierda(
                p, 
                f"Resolución: {doc.resolucion.numero} {doc.resolucion.fecha_desde.strftime('%Y-%m-%d')}", 
                margen, y
            )
            
            y = self.dibujar_texto_izquierda(
                p,
                f"Prefijo: {doc.resolucion.prefijo} del {doc.resolucion.consecutivo_desde} al {doc.resolucion.consecutivo_hasta}",
                margen, y
            )
        
        return y

    def dibujar_datos_electronicos(self, p, data, y, ancho, margen):
        doc = data['documento']
        
        if doc.cue or doc.qr:
            # Línea divisoria con menos espacio después
            y = self.dibujar_linea_divisoria(p, y, ancho, margen)
            y -= 5 * mm
            
            # Sección CUF y fecha
            if doc.cue:
                # CUF más compacto
                cue_para = Paragraph(f"CUFE: {doc.cue}", self.estilo_negrita)
                cue_para.wrapOn(p, ancho - 2*margen, 20 * mm)
                cue_para.drawOn(p, margen, y - cue_para.height)
                y -= cue_para.height + 4 * mm
                
                # Fecha más compacta
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                y = self.dibujar_texto_izquierda(p, "Fecha aceptación DIAN:", margen, y, negrita=True)
                y = self.dibujar_texto_izquierda(p, fecha, margen, y)
                y -= 10 * mm
            
            # Sección QR
            if doc.qr:
                qr_size = 20 * mm
                qr_x = (ancho - qr_size) / 2 - 5 * mm
                qr_y = y - qr_size
                
                # Dibujar QR
                qr_code = generar_qr(doc.qr)
                renderPDF.draw(qr_code, p, qr_x, qr_y)
                y -= qr_size + 2 * mm
                
                # Texto proveedor centrado exacto
                textos_proveedor = [
                    "Proveedor tecnológico KIAI S.A.S",
                    "Nit: 901337751 - 9"
                ]
                
                p.setFont("Courier-Bold", 7)
                for texto in textos_proveedor:
                    ancho_texto = p.stringWidth(texto, "Courier-Bold", 7)
                    p.drawString((ancho - ancho_texto)/2, y, texto)
                    y -= 4 * mm
        
        return y

    def dibujar_texto_centrado(self, p, texto, x, y, negrita=False, tamano=7):
        """Versión con Paragraph para manejo de multilínea"""
        estilo = self.estilo_negrita if negrita else self.estilo_normal
        estilo.fontSize = tamano
    
        para = Paragraph(texto, estilo)
        ancho_max = 70 * mm
        para.wrap(ancho_max, 50 * mm)
        pos_x = x - (para.width / 2)
        pos_y = y - para.height
        para.drawOn(p, pos_x, pos_y)
        return pos_y - 2

    def dibujar_texto_izquierda(self, p, texto, x, y, negrita=False, tamano=7):
        estilo = self.estilo_negrita if negrita else self.estilo_normal
        estilo.fontSize = tamano
        
        p.setFont(estilo.fontName, estilo.fontSize)
        p.drawString(x, y, texto)
        
        return y - estilo.fontSize - 2 * mm

    def dibujar_linea_divisoria(self, p, y, ancho, margen):
        p.setLineWidth(0.5)
        p.setDash([2, 2])
        p.line(margen, y, ancho - margen, y)
        p.setDash([])
        return y - 5 * mm