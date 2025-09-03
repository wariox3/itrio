from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY, TA_CENTER
from transporte.models.despacho import TteDespacho
from general.models.empresa import GenEmpresa
from decouple import config
from datetime import datetime
from utilidades.pdf_utilidades import PDFUtilidades

# Importa tu clase de utilidades

class FormatoManifiesto:
    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(letter))

        # Configurar coordenadas (en landscape, el ancho es mayor que el alto)
        width, height = landscape(letter)  # width = 792, height = 612 (en puntos)

        despacho = TteDespacho.objects.get(pk=despacho_id)
        empresa = GenEmpresa.objects.get(pk=1)
        
        def dibujar_formato():
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

            x = 10
            y = height - 80 
            tamano_cuadrado = 1 * inch

            # Dibujar la imagen sin los cuadros
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto', preserveAspectRatio=True)

            # Agregar información de la empresa al lado de la imagen
            p.setFont("Helvetica-Bold", 14)
            p.drawString(x + tamano_cuadrado + 50, y + 40, "MANIFIESTO ELECTRÓNICO DE CARGA")
            p.drawString(x + tamano_cuadrado + 50, y + 20, validarVacio(empresa.nombre_corto))
            p.drawString(x + tamano_cuadrado + 50, y, f"NIT: {validarVacio(empresa.numero_identificacion)} - {validarVacio(empresa.digito_verificacion)}")
            p.setFont("Helvetica", 12)
            p.drawString(x + tamano_cuadrado + 50, y - 10, validarVacio(empresa.direccion))
            p.drawString(x + tamano_cuadrado + 50, y - 20, validarVacio(empresa.telefono))
            p.drawString(x + tamano_cuadrado + 50, y - 30, f"{validarVacio(empresa.ciudad, 'nombre')} - {validarVacio(getattr(empresa.ciudad, 'estado', None), 'nombre')}")

            texto_legal = (
                "La impresión en soporte cartular (papel) de este acto "
                "administrativo producido por medios electrónicos en "
                "cumplimiento de la ley 527 de 1999 (Articulos 6 al 13) y "
                "de la ley 962 de 2005 (Articulo 6), es una reproducción "
                "del documento original que se encuentra en formato "
                "electrónico firmado digitalmente, cuya representación "
                "digital goza de autenticidad, integridad y no repudio"
            )
            
            styles = getSampleStyleSheet()
            estilo_legal = ParagraphStyle(
                'LegalStyle',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=7,
                alignment=TA_JUSTIFY,
                textColor='black',
                spaceAfter=0,
                spaceBefore=0,
                leading=6
            )
            
            # Crear el párrafo
            parrafo_legal = Paragraph(texto_legal, estilo_legal)
            
            # Definir posición y tamaño del párrafo (a la derecha de los datos)
            parrafo_x = width - 300
            parrafo_y = y + 10
            parrafo_width = 150
            parrafo_height = 60
            
            # Dibujar el párrafo en el canvas
            parrafo_legal.wrapOn(p, parrafo_width, parrafo_height)
            parrafo_legal.drawOn(p, parrafo_x, parrafo_y)

            # Bloque despacho - Ahora con celdas con bordes
            celda_x = x + 20  # Posición inicial X
            celda_y = y - 100  # Posición Y (más abajo)
            celda_ancho = 150  # Ancho de cada celda
            celda_alto = 35   # Alto de cada celda
            espacio_entre_celdas = 0  # Espacio entre celdas
            
            # FECHA EXPEDICIÓN - Con línea divisora
            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, celda_x, celda_y, celda_ancho, celda_alto, 
                "FECHA EXPEDICIÓN", 
                PDFUtilidades.formatear_fecha(despacho.fecha),
                con_linea_divisora=False
            )
            celda_x += espacio_entre_celdas
            
            if hasattr(despacho, 'despacho_tipo'):
                celda_x = PDFUtilidades.dibujar_celda_con_borde(
                    p, celda_x, celda_y, celda_ancho, celda_alto, 
                    "TIPO MANIFIESTO", validarVacio(despacho.despacho_tipo.nombre),
                    con_linea_divisora=False
                )
            celda_x += espacio_entre_celdas
            
            if hasattr(despacho, 'ciudad_origen'):
                # Obtener nombre de la ciudad
                nombre_ciudad = validarVacio(despacho.ciudad_origen, 'nombre')
                
                # Obtener nombre del estado (si existe)
                nombre_estado = ""
                if hasattr(despacho.ciudad_origen, 'estado') and despacho.ciudad_origen.estado:
                    nombre_estado = validarVacio(despacho.ciudad_origen.estado, 'nombre')
                
                # Concatenar ciudad y estado
                valor_completo = f"{nombre_ciudad}"
                if nombre_estado:
                    valor_completo += f" - {nombre_estado}"
                
                celda_x = PDFUtilidades.dibujar_celda_con_borde(
                    p, celda_x, celda_y, 220, celda_alto, 
                    "ORIGEN DEL VIAJE", valor_completo,
                    con_linea_divisora=False
                )
            celda_x += espacio_entre_celdas
            
            if hasattr(despacho, 'ciudad_destino'):
                # Obtener nombre de la ciudad
                nombre_ciudad = validarVacio(despacho.ciudad_destino, 'nombre')
                
                # Obtener nombre del estado (si existe)
                nombre_estado = ""
                if hasattr(despacho.ciudad_destino, 'estado') and despacho.ciudad_destino.estado:
                    nombre_estado = validarVacio(despacho.ciudad_destino.estado, 'nombre')
                
                # Concatenar ciudad y estado
                valor_completo = f"{nombre_ciudad}"
                if nombre_estado:
                    valor_completo += f" - {nombre_estado}"
                
                celda_x = PDFUtilidades.dibujar_celda_con_borde(
                    p, celda_x, celda_y, 220, celda_alto, 
                    "DESTINO DEL VIAJE", valor_completo,
                    con_linea_divisora=False
                )

            titulo_y = celda_y - celda_alto + 21
            ancho_total = width - 52  # Ancho total (márgenes de 20 a cada lado)

            # Dibujar la celda de título único
            PDFUtilidades.dibujar_celda_con_borde(
                p, 
                x + 20,           # Mismo margen izquierdo que las otras celdas
                titulo_y,         # Nueva posición Y (debajo de las otras celdas)
                ancho_total,      # Ancho completo
                14,       # Mismo alto que las otras celdas
                "INFORMACIÓN DEL VEHÍCULO Y CONDUCTOR",
                valor=None,       # Sin valor
                font_titulo="Helvetica-Bold",
                size_titulo=10,
                padding=5,
                con_linea_divisora=False,  # Sin línea divisora
                solo_titulo=True           # Modo solo título
            )

            nuevas_celdas_y = titulo_y - celda_alto 
            nuevo_celda_x = x + 20

            if hasattr(empresa, 'nombre_corto'):
                nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                    p, nuevo_celda_x, nuevas_celdas_y, 180, celda_alto, 
                    "TITULAR MANIFIESTO", validarVacio(empresa.nombre_corto),
                    con_linea_divisora=False
                )
            nuevo_celda_x += espacio_entre_celdas

            if hasattr(empresa, 'numero_identificacion'):
                nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                    p, nuevo_celda_x, nuevas_celdas_y, 180, celda_alto, 
                    "DOCUMENTO IDENTIFICACIÓN", validarVacio(empresa.numero_identificacion),
                    con_linea_divisora=False
                )
            nuevo_celda_x += espacio_entre_celdas

            if hasattr(empresa, 'direccion'):
                nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                    p, nuevo_celda_x, nuevas_celdas_y, 180, celda_alto, 
                    "DIRECCIÓN", validarVacio(empresa.direccion),
                    con_linea_divisora=False
                )
            nuevo_celda_x += espacio_entre_celdas

        dibujar_formato()
        p.showPage()
        p.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    
def validarVacio(value, attr=None):
    if value is None:
        return ""
    if attr:
        return str(getattr(value, attr, "") or "")
    return str(value)