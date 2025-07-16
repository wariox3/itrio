from general.models.empresa import GenEmpresa
from humano.models.contrato import HumContrato
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from decouple import config
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from datetime import datetime
from utilidades.utilidades import convertir_a_letras
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class FormatoCertificadoLaboral():

    def generar_pdf(self, id=None):  

        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except:
            locale.setlocale(locale.LC_TIME, 'spanish')

        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)  
        p.setTitle("certificado_laboral")
        empresa = GenEmpresa.objects.filter(pk=1).first()
        contrato = HumContrato.objects.select_related('contacto', 'cargo', 'contacto__identificacion').filter(id=id).first()

        def generar_pagina_certificado():
            # Configuración de la imagen
            region = config('DO_REGION')
            bucket = config('DO_BUCKET')
            entorno = config('ENV')
            imagen_defecto_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'
            imagen_empresa = empresa.imagen
            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{imagen_empresa}'
            
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

            # Dibujar logo
            x = 20
            y = 680
            tamano_cuadrado = 1 * inch
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')

            styles = getSampleStyleSheet()

            # Textos centrados
            p.setFont("Helvetica-Bold", 12)
            p.drawCentredString(x + 280, 650, "DEPARTAMENTO DE RECURSOS HUMANOS")
            p.drawCentredString(x + 280, 580, "CERTIFICA QUE:")
            

            estilo_espaciado = ParagraphStyle(
                'espaciado',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=12,
                alignment=TA_JUSTIFY,
                leading=14,
            )

            # Texto completo del certificado con espacios controlados
            texto_completo = f"""
            El señor (a) <b>{contrato.contacto.nombre_corto}</b>, identificado (a) con 
            {contrato.contacto.identificacion.nombre if contrato.contacto.identificacion else 'cédula de ciudadanía'} 
            No. <b>{contrato.contacto.numero_identificacion}</b>, labora en nuestra empresa 
            <b>{empresa.nombre_corto}</b> NIT <b>{empresa.numero_identificacion}</b> desde el 
            <b>{contrato.fecha_desde.strftime('%Y-%m-%d') if contrato.fecha_desde else 'fecha no especificada'}</b>, 
            desempeñándose en el cargo de <b>{contrato.cargo.nombre if contrato.cargo else 'cargo no especificado'}</b>.
            <br/><br/><br/>
            Devenga un salario básico mensual de <b>{convertir_a_letras(contrato.salario) if contrato.salario else 'SALARIO NO ESPECIFICADO'}</b> M/C 
            ({f"${contrato.salario:,.0f}" if contrato.salario else ''}) con un contrato {contrato.contrato_tipo.nombre}.
            <br/><br/><br/>
            Este certificado se expide en {empresa.ciudad.nombre} el {datetime.now().strftime('%d de %B de %Y')}.
            """

            parrafo_completo = Paragraph(texto_completo, estilo_espaciado)

            parrafo_completo.wrapOn(p, 500, 600)
            parrafo_completo.drawOn(p, x + 20, 380)
            
            y_position = 280 

            # Texto "Atentamente"
            p.setFont("Helvetica", 12)
            p.drawString(x + 20, y_position, "Atentamente,")

            y_position -= 100

            p.line(x + 20, y_position + 20, x + 280, y_position + 20)
            p.setFont("Helvetica-Bold", 12)
            p.drawString(x + 20, y_position, "DEPARTAMENTO DE RECURSOS HUMANOS")

        generar_pagina_certificado()            

        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes