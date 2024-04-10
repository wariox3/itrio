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

class FormatoCuentaCobro():

    def generar_pdf(self, data):  
        buffer = BytesIO()                              
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        estilo_helvetica = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8)
        elements = []
        elements.append(Paragraph("Hola mundo", estilo_helvetica))
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
