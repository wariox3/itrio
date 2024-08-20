from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from decouple import config
from general.formatos.encabezado import FormatoEncabezado
import locale

class FormatoNomina():
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, documento):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)                
        self.encabezado.generar_pdf(p)

        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id = documento.id).values(
            'concepto_id', 'concepto__nombre', 'detalle', 'cantidad', 'dias', 'porcentaje', 'devengado', 'deduccion')

        headers = ['COD', 'CONCEPTO', 'DETALLE', 'HORAS', 'DÍAS', '%', 'DEVENGADO', 'DEDUCCION']
        #data = [headers] + list(documento_detalles)
        x = 40
        y = 600
        alto_fila = 20
        ancho_columna = [30, 150, 80, 40, 40, 20, 70, 70]
        
        # Dibujar encabezados
        p.setFont("Helvetica", 10)
        #for i, header in enumerate(headers):
        #    p.drawString(x + sum(ancho_columna[:i]), y, header)   
        p.drawString(x + sum(ancho_columna[:0]), y, 'COD')
        p.drawString(x + sum(ancho_columna[:1]), y, 'CONCEPTO')
        p.drawString(x + sum(ancho_columna[:2]), y, 'DETALLE')            
        p.drawString(x + sum(ancho_columna[:3]), y, 'HORAS')
        p.drawString(x + sum(ancho_columna[:4]), y, 'DÍAS')
        p.drawString(x + sum(ancho_columna[:6]), y, '%')
        p.drawString(x + sum(ancho_columna[:7]), y, 'DEVENGADO')
        p.drawString(x + sum(ancho_columna[:8]), y, 'DEDUCCION')
        y -= alto_fila

        ylinea = y
        # Dibujar líneas de la tabla
        p.setStrokeColor(colors.black)
        p.setLineWidth(1)
        for i in range(len(documento_detalles) + 1):
            p.line(x, y, x + sum(ancho_columna), y)
            ylinea -= alto_fila
   
        
        # Dibujar datos de la tabla
        p.setFont("Helvetica", 8)
        for documento_detalle in documento_detalles:
            #for i, item in enumerate(fila):
            p.drawString(x + sum(ancho_columna[:0]), y, str(documento_detalle['concepto_id']))
            p.drawString(x + sum(ancho_columna[:1]), y, str(documento_detalle['concepto__nombre']))
            p.drawString(x + sum(ancho_columna[:2]), y, str(documento_detalle['detalle'] or ""))            
            p.drawRightString(x + sum(ancho_columna[:3]) + 30, y, f"{documento_detalle['cantidad']:.2f}")
            p.drawRightString(x + sum(ancho_columna[:4]) + 20, y, str(int(documento_detalle['dias'])))
            p.drawRightString(x + sum(ancho_columna[:5]) + 40, y, str(int(documento_detalle['porcentaje'])))
            p.drawRightString(x + sum(ancho_columna[:6]) + 120, y, f"{documento_detalle['devengado']:,.0f}")
            p.drawRightString(x + sum(ancho_columna[:7]) + 120, y, f"{documento_detalle['deduccion']:,.0f}")
            y -= alto_fila
        
        # Dibujar líneas verticales
        #y = height - 50 - row_height
        #for i in range(len(col_widths) + 1):
        #    p.line(x + sum(col_widths[:i]), height - 50 - (row_height * len(data)), x + sum(col_widths[:i]), height - 50)


        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
