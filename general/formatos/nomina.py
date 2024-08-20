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

        p.drawString(10,400,"Este es el cuerpo")
        documento_detalles = GenDocumentoDetalle.objects.filter(documento_id = documento.id).values_list('detalle', 'cantidad', 'precio')
        #for documento_detalle in documento_detalles:
        #    pass

        # Datos de la tabla
        headers = ['Descripción', 'Cantidad', 'Precio']
        data = [headers] + list(documento_detalles)

        width, height = letter
        # Configuración inicial
        x = 50
        y = height - 300
        row_height = 20
        col_widths = [200, 100, 100]
        
        # Dibujar encabezados
        p.setFont("Helvetica-Bold", 12)
        for i, header in enumerate(headers):
            p.drawString(x + sum(col_widths[:i]), y, header)        
        y -= row_height

        
        # Dibujar líneas de la tabla
        p.setStrokeColor(colors.black)
        p.setLineWidth(1)
        for i in range(len(data) + 1):
            p.line(x, y, x + sum(col_widths), y)
            y -= row_height
        y += row_height
        
        x = 50  # Resetear x para la segunda columna
        y = height - 50 - row_height  # Ajustar y para la fila de encabezado
        
        # Dibujar datos de la tabla
        p.setFont("Helvetica", 10)
        for row in data:
            for i, item in enumerate(row):
                p.drawString(x + sum(col_widths[:i]), y, str(item))
            y -= row_height
        
        # Dibujar líneas verticales
        y = height - 50 - row_height
        for i in range(len(col_widths) + 1):
            p.line(x + sum(col_widths[:i]), height - 50 - (row_height * len(data)), x + sum(col_widths[:i]), height - 50)


        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
