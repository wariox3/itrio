from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Frame, PageTemplate, BaseDocTemplate, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from io import BytesIO
from general.formatos.encabezado import FormatoEncabezado
from datetime import datetime
from general.models.contacto import GenContacto  
from general.models.empresa import GenEmpresa


class FormatoCertificadoRetencion:
    def __init__(self):
        self.encabezado = FormatoEncabezado()
        self.styles = getSampleStyleSheet()
        
    def obtener_datos_contacto(self, contacto_id):
        """Obtiene solo los datos necesarios del contacto"""
        try:
            contacto = GenContacto.objects.only('nombre_corto', 'numero_identificacion').get(id=contacto_id)
            return {
                'nombre': contacto.nombre_corto,
                'nit': contacto.numero_identificacion
            }
        except GenContacto.DoesNotExist:
            return {'nombre': 'CONTACTO NO ENCONTRADO', 'nit': 'N/A'}
        except Exception:
            return {'nombre': 'ERROR', 'nit': 'N/A'}

    def obtener_datos_empresa(self):
        """Obtiene ciudad y departamento de la empresa"""
        try:
            empresa = GenEmpresa.objects.select_related('ciudad').get(pk=1)
            ciudad_nombre = empresa.ciudad.nombre if empresa.ciudad else ''
            departamento = empresa.ciudad.estado.nombre if empresa.ciudad and empresa.ciudad.estado else ''
            return f"{ciudad_nombre.upper()} - {departamento.upper()}"
        except Exception:
            return "" 

    def generar_texto_certificado(self, fecha_desde, fecha_hasta, datos_contacto):
        """Genera el texto del certificado con los parámetros"""
        fecha_desde_fmt = datetime.strptime(fecha_desde, '%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_hasta_fmt = datetime.strptime(fecha_hasta, '%Y-%m-%d').strftime('%Y-%m-%d')
        ciudad_empresa = self.obtener_datos_empresa()
        
        texto = f"""
        Durante el año gravable {fecha_desde_fmt[:4]}, desde el {fecha_desde_fmt} hasta el {fecha_hasta_fmt}, 
        practicó en la ciudad de {ciudad_empresa} las siguientes retenciones a 
        <b>{datos_contacto['nombre']}</b> con NIT: <b>{datos_contacto['nit']}</b>
        """
        
        return texto.strip()

    def crear_tabla_resultados(self, resultados_json):
        """Crea una tabla con los resultados JSON"""
        if not resultados_json:
            return Paragraph("No se encontraron resultados.", self.styles['Normal'])
        
        headers = ["Concepto", "Monto sujeto a retención ($)", "Retenido y consignado ($)"]
        data = [headers]
        total_base = total_retenido = 0
        
        for registro in resultados_json:
            base = float(registro.get('base_retenido', 0) or 0)
            retenido = float(registro.get('retenido', 0) or 0)
            
            data.append([
                registro.get('cuenta_nombre', ''),
                f"${base:,.2f}",
                f"${retenido:,.2f}"
            ])
            
            total_base += base
            total_retenido += retenido
        
        data.append(["", f"${total_base:,.2f}", f"${total_retenido:,.2f}"])
        
        tabla = Table(data, colWidths=[8*cm, 4.5*cm, 4.5*cm])
        tabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (1, 0), (1, -1), 15),
            ('RIGHTPADDING', (1, 0), (1, -1), 15),
            ('LEFTPADDING', (2, 0), (2, -1), 15),
            ('RIGHTPADDING', (2, 0), (2, -1), 15),
        ]))
        
        return tabla

    def generar_pdf(self, fecha_desde, fecha_hasta, resultados_json, contacto_id):
        buffer = BytesIO()
        
        datos_contacto = self.obtener_datos_contacto(contacto_id)
        
        doc = BaseDocTemplate(
            buffer, 
            pagesize=letter,
            leftMargin=1.5*cm,
            rightMargin=1.5*cm,
            topMargin=4*cm,
            bottomMargin=2*cm
        )
        
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        
        def dibujar_encabezado(canvas, doc):
            self.encabezado.generar_pdf(canvas, "CERTIFICADO RETENCIÓN")
        
        template = PageTemplate(id='CertificadoTemplate', frames=frame, onPage=dibujar_encabezado)
        doc.addPageTemplates([template])
        
        estilo_base = ParagraphStyle(
            'BaseStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        contenido = []
        
        # Texto inicial del certificado
        texto_certificado = self.generar_texto_certificado(fecha_desde, fecha_hasta, datos_contacto)
        contenido.append(Paragraph(texto_certificado, estilo_base))
        contenido.append(Spacer(1, 0.3*inch))
        
        # Tabla de resultados
        if resultados_json:
            contenido.append(self.crear_tabla_resultados(resultados_json))
        else:
            contenido.append(Paragraph("<i>No se encontraron retenciones para el período seleccionado.</i>", estilo_base))
        
        contenido.append(Spacer(1, 0.3*inch))
        
        # Texto legal al final
        texto_legal = """
        Se expide este certificado en cumplimiento de lo establecido en el Artículo 381 del Estatuto Tributario. 
        Este Certificado no requiere firma autógrafa de acuerdo con el artículo 10 del Decreto Reglamentario 836 de 1991
        """
        contenido.append(Paragraph(texto_legal.strip(), estilo_base))
        
        doc.build(contenido)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes