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

            # Variables de posición inicial
            x = 10
            y = height - 80 
            tamano_cuadrado = 1 * inch

            # Dibujar la imagen sin los cuadros
            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto', preserveAspectRatio=True)

            # Agregar información de la empresa al lado de la imagen
            p.setFont("Helvetica-Bold", 13)
            p.drawString(x + tamano_cuadrado + 50, y + 40, "MANIFIESTO ELECTRÓNICO DE CARGA")
            p.drawString(x + tamano_cuadrado + 50, y + 25, validarVacio(empresa.nombre_corto))
            p.drawString(x + tamano_cuadrado + 50, y + 10, f"NIT: {validarVacio(empresa.numero_identificacion)}")
            p.setFont("Helvetica-Bold", 11)
            p.drawString(x + tamano_cuadrado + 50, y - 10, validarVacio(empresa.direccion))
            p.drawString(x + tamano_cuadrado + 50, y - 25, validarVacio(empresa.telefono))
            p.drawString(x + tamano_cuadrado + 50, y - 40, f"{validarVacio(empresa.ciudad, 'nombre')} - {validarVacio(getattr(empresa.ciudad, 'estado', None), 'nombre')}")

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

            # Ajustar posición Y para la siguiente sección (mover hacia abajo)
            y_seccion = y - 85  # Posición inicial para la sección de despacho

            # Bloque despacho - Ahora con celdas con bordes
            celda_x = x + 20  # Posición inicial X
            celda_y = y_seccion  # Posición Y
            celda_ancho = 150  # Ancho de cada celda
            celda_alto = 28   # Alto de cada celda
            espacio_entre_celdas = 0  # Espacio entre celdas

            # FECHA EXPEDICIÓN
            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, celda_x, celda_y, celda_ancho, celda_alto, 
                "FECHA EXPEDICIÓN", 
                PDFUtilidades.formatear_fecha(despacho.fecha),
                con_linea_divisora=False
            )
            celda_x += espacio_entre_celdas

            # TIPO MANIFIESTO
            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, celda_x, celda_y, celda_ancho, celda_alto, 
                "TIPO MANIFIESTO", obtener_valor_seguro(despacho, 'despacho_tipo', 'nombre'),
                con_linea_divisora=False
            )
            celda_x += espacio_entre_celdas

            # ORIGEN DEL VIAJE
            origen_ciudad = obtener_valor_seguro(despacho.ciudad_origen, 'nombre')
            origen_estado = obtener_valor_seguro(despacho.ciudad_origen, 'estado', 'nombre')
            valor_origen = f"{origen_ciudad}" + (f" - {origen_estado}" if origen_estado else "")

            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, celda_x, celda_y, 220, celda_alto, 
                "ORIGEN DEL VIAJE", valor_origen,
                con_linea_divisora=False
            )
            celda_x += espacio_entre_celdas

            # DESTINO DEL VIAJE
            destino_ciudad = obtener_valor_seguro(despacho.ciudad_destino, 'nombre')
            destino_estado = obtener_valor_seguro(despacho.ciudad_destino, 'estado', 'nombre')
            valor_destino = f"{destino_ciudad}" + (f" - {destino_estado}" if destino_estado else "")

            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, celda_x, celda_y, 220, celda_alto, 
                "DESTINO DEL VIAJE", valor_destino,
                con_linea_divisora=False
            )

            # Ajustar posición Y para la siguiente sección
            y_seccion = celda_y - celda_alto + 14

            # Título de sección
            titulo_y = y_seccion
            ancho_total = width - 52 
            PDFUtilidades.dibujar_celda_con_borde(
                p, x + 20, titulo_y, ancho_total, 14,
                "INFORMACIÓN DEL VEHÍCULO Y CONDUCTOR", None,
                font_titulo="Helvetica-Bold", size_titulo=9, padding=5,
                con_linea_divisora=False, solo_titulo=True
            )

            # Ajustar posición Y
            y_seccion = titulo_y - celda_alto
            nuevas_celdas_y = y_seccion
            nuevo_celda_x = x + 20

            # TITULAR MANIFIESTO
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, nuevas_celdas_y, 200, celda_alto, 
                "TITULAR MANIFIESTO", obtener_valor_seguro(despacho.vehiculo, 'poseedor', 'nombre_corto'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # DOCUMENTO IDENTIFICACIÓN
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, nuevas_celdas_y, 160, celda_alto, 
                "DOCUMENTO IDENTIFICACIÓN", validarVacio(empresa.numero_identificacion),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # DIRECCIÓN
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, nuevas_celdas_y, 160, celda_alto, 
                "DIRECCIÓN", validarVacio(empresa.direccion),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # TELÉFONO
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, nuevas_celdas_y, 100, celda_alto, 
                "TELÉFONO", validarVacio(empresa.telefono),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # CIUDAD
            ciudad_empresa = obtener_valor_seguro(empresa.ciudad, 'nombre')
            estado_empresa = obtener_valor_seguro(empresa.ciudad, 'estado', 'nombre')
            valor_ciudad = f"{ciudad_empresa}" + (f" - {estado_empresa}" if estado_empresa else "")

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, nuevas_celdas_y, 120, celda_alto, 
                "CIUDAD", valor_ciudad,
                con_linea_divisora=False
            )

            # Segunda fila de información del vehículo
            y_seccion = nuevas_celdas_y - celda_alto
            nuevo_celda_x = x + 20

            # PLACA
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 75, celda_alto, 
                "PLACA", obtener_valor_seguro(despacho.vehiculo, 'placa'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # MARCA
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 75, celda_alto, 
                "MARCA", obtener_valor_seguro(despacho.vehiculo, 'marca', 'nombre'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # PLACA SEMI REMOLQUE
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 120, celda_alto, 
                "PLACA SEMI REMOLQUE", obtener_valor_seguro(despacho.remolque, 'placa'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # CONFIGURACIÓN
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 90, celda_alto, 
                "CONFIGURACIÓN", obtener_valor_seguro(despacho.vehiculo, 'configuracion', 'codigo'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 60, celda_alto, 
                "PESO VACÍO", obtener_valor_seguro(despacho.vehiculo, 'peso_vacio'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 60, celda_alto, 
                "N PÓLIZA", obtener_valor_seguro(despacho.vehiculo, 'poliza'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 140, celda_alto, 
                "COMPAÑIA SEGUROS SOAT", obtener_valor_seguro(""),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 120, celda_alto, 
                "F/VENCE SOAT", 
                PDFUtilidades.formatear_fecha(obtener_valor_seguro(despacho.vehiculo, 'vence_poliza')) if obtener_valor_seguro(despacho.vehiculo, 'vence_poliza') else "",
                con_linea_divisora=False,
            )
            nuevo_celda_x += espacio_entre_celdas

            # Tercera fila - Conductor
            y_seccion = y_seccion - celda_alto
            nuevo_celda_x = x + 20

            # CONDUCTOR
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 180, celda_alto, 
                "CONDUCTOR", obtener_valor_seguro(despacho.conductor, 'nombre_corto'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 150, celda_alto, 
                "DOCUMENTO IDENTIFICACIÓN", obtener_valor_seguro(despacho.conductor, 'numero_identificacion'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 170, celda_alto, 
                "DIRECCIÓN", obtener_valor_seguro(despacho.conductor, 'direccion'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 60, celda_alto, 
                "TELÉFONO", obtener_valor_seguro(despacho.conductor, 'telefono'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas


            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 60, celda_alto, 
                "N LICENCIA", obtener_valor_seguro(despacho.conductor, 'telefono'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # DESTINO DEL VIAJE
            ciudad_conductor = obtener_valor_seguro(despacho.conductor.ciudad, 'nombre')
            estado_conductor = obtener_valor_seguro(despacho.conductor.ciudad, 'estado', 'nombre')
            valor_destino = f"{ciudad_conductor}" + (f" - {estado_conductor}" if estado_conductor else "")

            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 120, celda_alto, 
                "CIUDAD", valor_destino,
                con_linea_divisora=False
            )

            # Cuarta fila - Poseedor
            y_seccion = y_seccion - celda_alto
            nuevo_celda_x = x + 20

            # POSEEDOR O TENER VEHÍCULO
            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 180, celda_alto, 
                "POSEEDOR O TENER VEHÍCULO", obtener_valor_seguro(despacho.vehiculo, 'poseedor', 'nombre_corto'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 150, celda_alto, 
                "DOCUMENTO IDENTIFICACIÓN", obtener_valor_seguro(despacho.vehiculo.poseedor, 'numero_identificacion'),
                con_linea_divisora=False
            )

            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 170, celda_alto, 
                "DIRECCIÓN", obtener_valor_seguro(despacho.vehiculo.poseedor, 'direccion'),
                con_linea_divisora=False
            )
            
            nuevo_celda_x += espacio_entre_celdas

            nuevo_celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 60, celda_alto, 
                "TELÉFONO", obtener_valor_seguro(despacho.vehiculo.poseedor, 'telefono'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # DESTINO DEL VIAJE
            ciudad_poseedor = obtener_valor_seguro(despacho.vehiculo.poseedor.ciudad, 'nombre')
            estado_poseedor = obtener_valor_seguro(despacho.vehiculo.poseedor.ciudad, 'estado', 'nombre')
            valor_destino = f"{ciudad_poseedor}" + (f" - {estado_poseedor}" if estado_poseedor else "")

            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 180, celda_alto, 
                "CIUDAD", valor_destino,
                con_linea_divisora=False
            )

            y_seccion = y_seccion - celda_alto + 14

            titulo_y = y_seccion
            ancho_total = width - 52 
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                x + 20,
                titulo_y,
                ancho_total,
                14,
                "INFORMACIÓN MERCANCÍA TRANSPORTADA",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
            )


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

def obtener_valor_seguro(objeto, *atributos):
    """
    Obtiene el valor de atributos anidados de forma segura.
    Ejemplo: obtener_valor_seguro(despacho.vehiculo, 'marca', 'nombre')
    """
    valor_actual = objeto
    for atributo in atributos:
        if valor_actual is None or not hasattr(valor_actual, atributo):
            return ""
        valor_actual = getattr(valor_actual, atributo)
        if valor_actual is None:
            return ""
    return str(valor_actual)