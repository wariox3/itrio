from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from transporte.models.despacho import TteDespacho
from general.models.empresa import GenEmpresa
from decouple import config

class FormatoManifiesto:
    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(letter))

        # Configurar coordenadas (en landscape, el ancho es mayor que el alto)
        width, height = landscape(letter)  # width = 792, height = 612 (en puntos)

        empresa = GenEmpresa.objects.get(pk=1)
        
        def draw_header():
            region = config('DO_REGION')
            bucket = config('DO_BUCKET')
            entorno = config('ENV')

            imagen_defecto_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'

            # Intenta cargar la imagen desde la URL
            imagen_empresa = empresa.imagen

            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/{imagen_empresa}'
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

            # Posicionar la imagen en la esquina superior izquierda con menos margen
            x = 10  # Muy cerca del borde izquierdo (10 puntos en lugar de 24)
            y = height - 80  # Posicionar cerca del borde superior
            tamano_cuadrado = 1 * inch

            # Dibujar la imagen sin los cuadros
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto', preserveAspectRatio=True)

            # Agregar información de la empresa al lado de la imagen
            p.setFont("Helvetica-Bold", 14)
            p.drawString(x + tamano_cuadrado + 10, y + 40, "MANIFIESTO ELECTRÓNICO DE CARGA")
            p.drawString(x + tamano_cuadrado + 10, y + 20, f"RUT: {empresa.numero_identificacion}")
            p.setFont("Helvetica", 10)
            p.drawString(x + tamano_cuadrado + 10, y, f"Dirección: {empresa.direccion}")

        draw_header()
        p.showPage()
        p.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes