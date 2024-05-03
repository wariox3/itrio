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
import locale

class FormatoPrueba():

    def generar_pdf(self, data):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)
                
        estilo_letra = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8)
        informacionPago = Paragraph("<b>INFORMACIÓN DE PAGO: </b>", estilo_letra)
        comentario = Paragraph("<b>COMENTARIOS: </b>" +  str(data['comentario']), estilo_letra)

        qr = data['qr'] if (data['qr'] is not None) else ""        
        imagen_qr = generar_qr(qr)
        renderPDF.draw(imagen_qr, p, 340, 125)
        
        
        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
