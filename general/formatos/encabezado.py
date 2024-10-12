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

import locale

class FormatoEncabezado():

    def generar_pdf(self, p):
        region = config('DO_REGION')
        bucket = config('DO_BUCKET')  
        empresa = GenEmpresa.objects.get(pk=1)
        
        logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{empresa.imagen}'
        try:
            logo = ImageReader(logo_url)
            p.drawImage(logo, 10, 680, width=100, height=100, mask='auto')
        except Exception as e:
            pass
        p.setFont("Helvetica", 10)
        p.drawString(120,760, "COMPORBANTE DE PAGO DE NÓMINA")
        p.drawString(120,740, empresa.nombre_corto or "")
        p.drawString(120,725, empresa.numero_identificacion or "")
        p.drawString(120,710, empresa.direccion or "")
        p.drawString(120,695, empresa.telefono or "")

    
