from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY, TA_CENTER
from transporte.models.despacho import TteDespacho
from transporte.models.despacho_detalle import TteDespachoDetalle
from general.models.empresa import GenEmpresa
from decouple import config
from datetime import datetime
from utilidades.pdf_utilidades import PDFUtilidades
from utilidades.utilidades import convertir_a_letras
from utilidades.utilidades import generar_qr
from reportlab.graphics import renderPDF

class FormatoManifiesto:
    def generar_pdf(self, despacho_id):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(letter))

        # Configurar coordenadas (en landscape, el ancho es mayor que el alto)
        width, height = landscape(letter)  # width = 792, height = 612 (en puntos)

        despacho = TteDespacho.objects.get(pk=despacho_id)
        empresa = GenEmpresa.objects.get(pk=1)
        detalles_despacho = TteDespachoDetalle.objects.filter(despacho_id=despacho_id)
        
        def generar_encabezado():
            """Genera el encabezado que se repetirá en todas las páginas"""
            region = config('DO_REGION')
            bucket = config('DO_BUCKET')
            entorno = config('ENV')

            imagen_defecto_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'

            # Intenta cargar la imagen desde la URL
            imagen_empresa = empresa.imagen

            logo_url = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/empresa/logo_defecto.jpg'
            try:
                logo = ImageReader(logo_url)
            except Exception as e:
                logo_url = imagen_defecto_url
                logo = ImageReader(logo_url)

 
            comentario = despacho.comentario if hasattr(despacho, 'comentario') else ''
        
            if isinstance(comentario, str):
                texto_comentario = "Obs:" + " " + comentario[:20]
            else:
                texto_comentario = ''
            
            contenido_qr = f"MEC:{despacho.numero_rndc if hasattr(despacho, 'numero_rndc') else ''}\n"
            contenido_qr += f"Fecha:{despacho.fecha_registro.strftime('%Y-%m-%d') if hasattr(despacho, 'fecha_registro') and despacho.fecha_registro else ''}\n"
            contenido_qr += f"Placa:{despacho.vehiculo.placa if hasattr(despacho.vehiculo, 'placa') and despacho.vehiculo.placa else ''}\n"
            contenido_qr += f"Remolque:{despacho.remolque.placa if hasattr(despacho.remolque, 'placa') and despacho.remolque.plcada else ''}\n"
            contenido_qr += f"Orig:{despacho.ciudad_origen.nombre if hasattr(despacho.ciudad_origen, 'nombre') and despacho.ciudad_origen.nombre else ''}\n"
            contenido_qr += f"Dest:{despacho.ciudad_destino.nombre if hasattr(despacho.ciudad_destino, 'nombre') and despacho.ciudad_destino.nombre else ''}\n"
            contenido_qr += "Mercancia:'VARIOS'\n"
            contenido_qr += f"Conductor:{despacho.conductor.nombre_corto if hasattr(despacho.conductor, 'nombre_corto') and despacho.conductor.nombre_corto else ''}\n"
            contenido_qr += f"Empresa:{empresa.nombre_corto if empresa else ''}\n"
            contenido_qr += f"{texto_comentario}\n"
            contenido_qr += "Seguro:\n"

            qr_code_drawing = generar_qr(contenido_qr)

            renderPDF.draw(qr_code_drawing, p, 680, 520)                

            # Variables de posición inicial
            x = 10
            y = height - 80 
            tamano_cuadrado = 1 * inch

            # Dibujar la imagen sin los cuadros
            p.drawImage(logo, 20, y - 40, width=tamano_cuadrado + 40, height=tamano_cuadrado+ 40, mask='auto', preserveAspectRatio=True)

            # Agregar información de la empresa al lado de la imagen
            p.setFont("Helvetica-Bold", 12)
            p.drawString(x + tamano_cuadrado + 50, y + 45, "MANIFIESTO ELECTRÓNICO DE CARGA")
            p.drawString(x + tamano_cuadrado + 50, y + 30, validarVacio(empresa.nombre_corto))
            p.drawString(x + tamano_cuadrado + 50, y + 15, f"NIT: {validarVacio(empresa.numero_identificacion)}")
            p.setFont("Helvetica-Bold", 10)
            p.drawString(x + tamano_cuadrado + 50, y, validarVacio(empresa.direccion))
            p.drawString(x + tamano_cuadrado + 50, y - 15, validarVacio(empresa.telefono))
            p.drawString(x + tamano_cuadrado + 50, y - 30, f"{validarVacio(empresa.ciudad, 'nombre')} - {validarVacio(getattr(empresa.ciudad, 'estado', None), 'nombre')}")

            # Tamaños para las nuevas imágenes (primera más grande)
            tamano_imagen1 = 1.4 * inch
            tamano_imagen2 = 1.4 * inch
            # Posición de la primera imagen (a la derecha de la dirección, un poco más abajo)
            x_imagen1 = x + tamano_cuadrado + 220  # Ajusta este valor según el espacio necesario
            y_imagen1 = y - 85  # Un poco más abajo que la dirección

            # Posición de la segunda imagen (a la derecha de la primera)
            x_imagen2 = x_imagen1 + tamano_imagen1 + 10  # A la derecha de la primera imagen
            y_imagen2 = y_imagen1 + (tamano_imagen1 - tamano_imagen2) / 2  # Centrada verticalmente respecto a la primera

            url_imagen1 = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/recursos/ministerio_transporte_2024.png'
            url_imagen2 = f'https://{bucket}.{region}.digitaloceanspaces.com/itrio/{entorno}/recursos/vigilado_supertransporte_2024.png'

            try:
                # Cargar y dibujar primera imagen nueva (más grande)
                imagen1 = ImageReader(url_imagen1)
                p.drawImage(imagen1, x_imagen1, y_imagen1, 
                            width=tamano_imagen1, 
                            height=tamano_imagen1, 
                            mask='auto', 
                            preserveAspectRatio=True)
            except Exception as e:
                print(f"Error cargando imagen 1: {e}")

            try:
                # Cargar y dibujar segunda imagen nueva (más pequeña, a la derecha de la primera)
                imagen2 = ImageReader(url_imagen2)
                p.drawImage(imagen2, x_imagen2, y_imagen2, 
                            width=tamano_imagen2, 
                            height=tamano_imagen2, 
                            mask='auto', 
                            preserveAspectRatio=True)
            except Exception as e:
                print(f"Error cargando imagen 2: {e}")


            texto_legal = (
                "La impresión en soporte cartular (papel) de este acto "
                "administrativo producido por medios electrónicos en "
                "cumplimiento de la ley 527 de 1999 (Articulos 6 al 13) y "
                "de la ley 962 de 2005 (Articulo 6), es una reproducción "
                "del documento original que se encuentra en formato "
                "electrónico firmado digitalmente, cuya representación "
                "digital goza de autenticidad, integridad y no repudio."
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
            parrafo_x = width - 265
            parrafo_y = y + 10
            parrafo_width = 150
            parrafo_height = 60
            
            # Dibujar el párrafo en el canvas
            parrafo_legal.wrapOn(p, parrafo_width, parrafo_height)
            parrafo_legal.drawOn(p, parrafo_x, parrafo_y)

            PDFUtilidades.dibujar_celda_con_borde(
                p, 530, 512, 120, 10, 
                "MANIFIESTO:", 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 650, 512, 120, 10, 
                obtener_valor_seguro(despacho, 'numero'), 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="derecha",                
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 530, 502, 120, 10, 
                "AUTORIZACIÓN RNDC:", 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="izquierda",                
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 650, 502, 120, 10, 
                obtener_valor_seguro(despacho, 'numero_rndc'), 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="derecha",                                
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 530, 492, 120, 10, 
                "DESPACHO:", 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="izquierda",                
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 650, 492, 120, 10, 
                obtener_valor_seguro(despacho, 'id'), 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="derecha",                                
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 530, 482, 120, 10, 
                "LLAVE:", 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="izquierda",                
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p, 650, 482, 120, 10, 
                obtener_valor_seguro(''), 
                con_linea_divisora=False,
                font_titulo="Helvetica-Bold", size_titulo=8, padding=5,
                solo_titulo=True,
                alineacion_titulo="derecha",                                
            )            

            # Retornar la posición Y después del encabezado para continuar con el contenido
            return y - 85

        def dibujar_informacion_general(y_seccion):
            """Dibuja la información general que va solo en la primera página"""
            # Bloque despacho - Ahora con celdas con bordes
            celda_x = 30  # Posición inicial X (x + 20)
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
                p, 30, titulo_y, ancho_total, 14,
                "INFORMACIÓN DEL VEHÍCULO Y CONDUCTOR", None,
                font_titulo="Helvetica-Bold", size_titulo=9, padding=5,
                con_linea_divisora=False, solo_titulo=True
            )

            # Ajustar posición Y
            y_seccion = titulo_y - celda_alto
            nuevas_celdas_y = y_seccion
            nuevo_celda_x = 30

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
            nuevo_celda_x = 30

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
            nuevo_celda_x = 30

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
                "N LICENCIA", obtener_valor_seguro(despacho.conductor, 'numero_licencia'),
                con_linea_divisora=False
            )
            nuevo_celda_x += espacio_entre_celdas

            # CIUDAD CONDUCTOR
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
            nuevo_celda_x = 30

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

            # CIUDAD POSEEDOR
            ciudad_poseedor = obtener_valor_seguro(despacho.vehiculo.poseedor.ciudad, 'nombre')
            estado_poseedor = obtener_valor_seguro(despacho.vehiculo.poseedor.ciudad, 'estado', 'nombre')
            valor_destino = f"{ciudad_poseedor}" + (f" - {estado_poseedor}" if estado_poseedor else "")

            celda_x = PDFUtilidades.dibujar_celda_con_borde(
                p, nuevo_celda_x, y_seccion, 180, celda_alto, 
                "CIUDAD", valor_destino,
                con_linea_divisora=False
            )

            # Retornar la posición Y después de toda la información general
            return y_seccion - 14

        def dibujar_tabla_mercancias(y_inicio, detalles_pagina, dibujar_vacia=False, es_pagina_adicional=False):
            """Dibuja la tabla de mercancías con los detalles proporcionados"""
            # Configuración de la tabla
            altura_fila = 14
            altura_encabezado_superior = 14
            x_inicio = 30
            ancho_total = width - 60
            
            # Anchos de columnas (ajustados para landscape)
            anchos_columnas = [50, 70, 25, 50, 40, 45, 90, 50, 160, 160]
            
            # ENCABEZADO SUPERIOR
            encabezados_superiores = ["INFORMACIÓN MERCANCÍA", "INFORMACIÓN REMITENTE", "INFORMACIÓN DESTINATARIO"]
            anchos_encabezado_superior = [370, 210, 160]
            
            # ENCABEZADO INFERIOR
            encabezados_inferiores = ["REMESA", "DOCUMENTO", "UM", "FEC", "UND", "PES", "DESTINO", "EMPAQUE", "NIT/CC Nombre/Razon Social", "NIT/CC Nombre/Razon Social"]
            
            # Dibujar ENCABEZADO SUPERIOR
            y_actual = y_inicio + 6
            x_actual = x_inicio
            
            p.setFont("Helvetica-Bold", 9)
            for i, encabezado in enumerate(encabezados_superiores):
                p.rect(x_actual, y_actual, anchos_encabezado_superior[i], altura_encabezado_superior)
                p.drawCentredString(x_actual + anchos_encabezado_superior[i] / 2, y_actual + 5, encabezado)
                x_actual += anchos_encabezado_superior[i]
            
            # Dibujar ENCABEZADO INFERIOR
            y_actual -= altura_encabezado_superior
            x_actual = x_inicio
            
            p.setFont("Helvetica-Bold", 9)
            for i, encabezado in enumerate(encabezados_inferiores):
                p.rect(x_actual, y_actual, anchos_columnas[i], altura_fila)
                texto = encabezado
                if len(texto) > 15:
                    p.setFont("Helvetica-Bold", 9)
                    p.drawCentredString(x_actual + anchos_columnas[i] / 2, y_actual + 5, texto)
                    p.setFont("Helvetica-Bold", 9)
                else:
                    p.drawCentredString(x_actual + anchos_columnas[i] / 2, y_actual + 5, texto)
                x_actual += anchos_columnas[i]
            
            # Dibujar filas de datos
            y_actual -= altura_fila
            
            if not dibujar_vacia:
                # Dibujar registros reales - SIN LIMITACIÓN, confiamos en la lógica de paginación
                for detalle in detalles_pagina:
                    # Solo verificar si nos estamos saliendo de la página (como medida de seguridad)
                    if y_actual < 50:  # Margen inferior de seguridad
                        # Dibujar mensaje de continuación pero NO romper el bucle
                        y_actual -= altura_fila
                        continue
                        
                    x_actual = x_inicio
                    p.setFont("Helvetica", 8)
                    
                    # REMESA
                    p.rect(x_actual, y_actual, anchos_columnas[0], altura_fila)
                    p.drawString(x_actual + 2, y_actual + 5, validarVacio(detalle.guia_id)[:15] if detalle.guia_id else "")
                    x_actual += anchos_columnas[0]
                    
                    # DOCUMENTO
                    p.rect(x_actual, y_actual, anchos_columnas[1], altura_fila)
                    p.drawString(x_actual + 2, y_actual + 5, validarVacio(detalle.guia.documento)[:15] if detalle.guia.documento else "")
                    x_actual += anchos_columnas[1]
                    
                    # UM (Unidad de Medida)
                    p.rect(x_actual, y_actual, anchos_columnas[2], altura_fila)
                    um = obtener_valor_seguro(detalle, 'unidad_medida', 'codigo') if hasattr(detalle, 'unidad_medida') else ""
                    p.drawCentredString(x_actual + anchos_columnas[2] / 2, y_actual + 5, um[:5] if um else "")
                    x_actual += anchos_columnas[2]
                    
                    # FEC (Fecha)
                    p.rect(x_actual, y_actual, anchos_columnas[3], altura_fila)
                    fecha_str = PDFUtilidades.formatear_fecha(detalle.guia.fecha) if hasattr(detalle.guia, 'fecha') and detalle.guia.fecha else ""
                    p.drawCentredString(x_actual + anchos_columnas[3] / 2, y_actual + 5, fecha_str)
                    x_actual += anchos_columnas[3]
                    
                    # UND (Unidades)
                    p.rect(x_actual, y_actual, anchos_columnas[4], altura_fila)
                    und = str(detalle.unidades) if hasattr(detalle, 'unidades') and detalle.unidades else "0"
                    p.drawCentredString(x_actual + anchos_columnas[4] / 2, y_actual + 5, und)
                    x_actual += anchos_columnas[4]
                    
                    # PES (Peso)
                    p.rect(x_actual, y_actual, anchos_columnas[5], altura_fila)
                    peso = str(detalle.peso) if hasattr(detalle, 'peso') and detalle.peso else "0"
                    p.drawCentredString(x_actual + anchos_columnas[5] / 2, y_actual + 5, peso)
                    x_actual += anchos_columnas[5]
                    
                    # DESTINO
                    p.rect(x_actual, y_actual, anchos_columnas[6], altura_fila)
                    destino_ciudad = obtener_valor_seguro(detalle.guia, 'ciudad_destino', 'nombre') if hasattr(detalle.guia, 'ciudad_destino') and detalle.guia.ciudad_destino else ""
                    p.drawString(x_actual + 2, y_actual + 5, destino_ciudad[:25] if destino_ciudad else "")
                    x_actual += anchos_columnas[6]
                    
                    # EMPAQUE
                    p.rect(x_actual, y_actual, anchos_columnas[7], altura_fila)
                    empaque = obtener_valor_seguro(detalle.guia, 'empaque', 'nombre') if hasattr(detalle, 'guia') and detalle.guia else ""
                    p.drawString(x_actual + 2, y_actual + 5, empaque[:10] if empaque else "")
                    x_actual += anchos_columnas[7]
                    
                    # NIT/CC REMITENTE
                    p.rect(x_actual, y_actual, anchos_columnas[8], altura_fila)
                    remitente_info = ""
                    if hasattr(detalle.guia, 'remitente') and detalle.guia.remitente:
                        nit = obtener_valor_seguro(detalle.guia.remitente, 'numero_identificacion', '')
                        nombre = obtener_valor_seguro(detalle.guia.remitente, 'nombre_corto', '')
                        remitente_info = f"{nit} {nombre}"[:25]
                    p.drawString(x_actual + 2, y_actual + 5, remitente_info)
                    x_actual += anchos_columnas[8]
                    
                    # NIT/CC DESTINATARIO
                    p.rect(x_actual, y_actual, anchos_columnas[9], altura_fila)
                    destinatario_info = ""
                    if hasattr(detalle.guia, 'destinatario') and detalle.guia.destinatario:
                        nit = obtener_valor_seguro(detalle.guia.destinatario, 'numero_identificacion', '')
                        nombre = obtener_valor_seguro(detalle.guia.destinatario, 'nombre_corto', '')
                        destinatario_info = f"{nit} {nombre}"[:25]
                    p.drawString(x_actual + 2, y_actual + 5, destinatario_info)
                    
                    y_actual -= altura_fila
                            
            else:
                # DIBUJAR TABLA VACÍA (solo primera página cuando hay más de 5 registros)
                altura_total_vacia = altura_fila * 5
                p.rect(x_inicio, y_actual - altura_total_vacia + altura_fila, 740, altura_total_vacia)
                y_actual -= altura_total_vacia
                return y_actual
            
            return y_actual

        def dibujar_informacion_final(y_inicio):
            """Dibuja la información final que va solo en la primera página"""
            celda_alto = 28
            y_actual = y_inicio  # Espacio después de la tabla
            alto = 14
            
            # OBSERVACIONES
            titulo_y = y_actual
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                300,
                alto,
                "VALORES",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y,
                210,
                alto,
                "CARGUE/DESCARGUE",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                540,
                titulo_y,
                230,
                alto,
                "OBSERVACIONES",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
            )
            
            titulo_y = y_actual - alto
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "VALOR PAGO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(despacho.pago, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            
            p.rect(190, titulo_y - 28, 140, 42)

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y - 14,
                52,
                28,
                "LUGAR:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=False,
            )

            p.rect(382, titulo_y - 14, 52, 28)

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                434,
                titulo_y - 14,
                54,
                28,
                "FECHA:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=False,
            )

            p.rect(488, titulo_y - 14, 52, 28)

            # Usar la misma función que usas en otras partes del código
            PDFUtilidades.dibujar_celda_con_borde(
                p, 
                540,
                titulo_y - 28,     # y
                230,          # ancho
                42,           # alto
                "",           # título (vacío)
                "",
                con_linea_divisora=False,
                font_titulo="Helvetica", 
                size_titulo=7,
                font_valor="Helvetica",
                size_valor=7,
                padding=5,
                alineacion_titulo="izquierda",
                alineacion_valor="justificado"  # o "izquierda" según prefieras
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
            parrafo_legal = Paragraph(despacho.comentario, estilo_legal)
            
            # Definir posición y tamaño del párrafo (a la derecha de los datos)
            parrafo_x = width - 235
            parrafo_y = titulo_y
            parrafo_width = 200
            parrafo_height = 60
            
            # Dibujar el párrafo en el canvas
            parrafo_legal.wrapOn(p, parrafo_width, parrafo_height)
            parrafo_legal.drawOn(p, parrafo_x, parrafo_y)                 

            titulo_y = y_actual - 28

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "RET FUENTE:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            titulo_y = y_actual - 42

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "RET ICA:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y,
                210,
                14,
                "CARGUE PAGADO POR:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            titulo_y = y_actual - 56

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "TOTAL:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(despacho.pago, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                190,
                titulo_y,
                70,
                14,
                "C_PAGO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                260,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y,
                210,
                14,
                "CONDUCTOR",
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                620,
                titulo_y,
                80,
                14,
                "UNIDADES:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )     

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                700,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(despacho.unidades, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
            )              

            titulo_y = y_actual - 70

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "ANTICIPO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                190,
                titulo_y,
                70,
                14,
                "C_ENTREGA:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                260,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(despacho.cobro_entrega, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y,
                210,
                14,
                "DESCARGUE PAGADO POR:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            ) 

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                620,
                titulo_y,
                80,
                14,
                "PESO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )     

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                700,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(despacho.peso, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
            )                      

            titulo_y = y_actual - 84

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "NETO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                190,
                titulo_y,
                70,
                14,
                "RECAUDO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                260,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(despacho.recaudo, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y,
                210,
                14,
                "CONDUCTOR",
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            ) 

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                620,
                titulo_y,
                80,
                14,
                "GUIAS:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )     

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                700,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(despacho.guias, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
            )                                   

            titulo_y = y_actual - 98

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                80,
                14,
                "SALDO:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                110,
                titulo_y,
                80,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                190,
                titulo_y,
                70,
                14,
                "SALDO PEND:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                260,
                titulo_y,
                70,
                14,
                PDFUtilidades.formatear_numero(0, decimales=0, separador_miles=','),
                valor=None,
                font_titulo="Helvetica",
                size_titulo=8,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
                formatear_como_numero=True,
            ) 

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                330,
                titulo_y,
                210,
                14,
                "ASEGURADORA:",
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )     

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                620,
                titulo_y,
                80,
                14,
                "CE:",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )     

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                700,
                titulo_y,
                70,
                14,
                "0",
                valor=None,
                font_titulo="Helvetica",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="derecha",
            )                       

            titulo_y = y_actual - 112      

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                740,
                14,
                f"EN CASO DE CUALQUIER NOVEDAD CON SEGURIDAD COMUNICARSE CON EL TELÉFONO: {validarVacio(empresa.telefono)}",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="centro",
            )   

            titulo_y = y_actual - 126      

            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                740,
                14,
                f"VALOR TOTAL EN LETRAS: {convertir_a_letras(despacho.pago)}",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=True,
                alineacion_titulo="izquierda",
            )  

            titulo_y = y_actual - 160

            # PRECINTOS
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
                titulo_y,
                250,
                34,
                "PRECINTOS:",
                valor=validarVacio(despacho.precinto),
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=False,
                alineacion_titulo="izquierda",
            )
            
            # FIRMA Y HUELLA TITULAR MANIFIESTO
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                280,
                titulo_y,
                250,
                34,
                "FIRMA Y HUELLA TITULAR MANIFIESTO",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=False,
                alineacion_titulo="centro",
            )
            
            # FIRMA Y HUELLA DEL CONDUCTOR
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                530,
                titulo_y,
                240,
                34,
                "FIRMA Y HUELLA DEL CONDUCTOR",
                valor=None,
                font_titulo="Helvetica-Bold",
                size_titulo=9,
                padding=5,
                con_linea_divisora=False,
                solo_titulo=False,
                alineacion_titulo="centro",
            )    
               

        # Lógica principal para manejar múltiples páginas CORREGIDA
        total_detalles = len(detalles_despacho)

        # Calcular páginas necesarias CORRECTAMENTE
        max_filas_primera_pagina = 5  # Máximo en primera página
        max_filas_paginas_adicionales = 32  # Máximo en páginas adicionales

        # Determinar si debemos mostrar tabla vacía en primera página
        mostrar_tabla_vacia_primera_pagina = total_detalles > max_filas_primera_pagina

        if mostrar_tabla_vacia_primera_pagina:
            # Si hay más de 5 detalles, primera página será vacía
            paginas_necesarias = 1  # Siempre tendremos al menos la primera página vacía
            
            # Calcular páginas adicionales para los detalles
            paginas_adicionales = (total_detalles + max_filas_paginas_adicionales - 1) // max_filas_paginas_adicionales
            paginas_necesarias += paginas_adicionales
        else:
            # Si hay 5 o menos detalles, todo va en la primera página
            paginas_necesarias = 1

        # Generar páginas
        for pagina in range(paginas_necesarias):
            # Generar encabezado para cada página
            y_actual = generar_encabezado()
            
            # En la primera página, dibujar toda la información general
            if pagina == 0:
                y_actual = dibujar_informacion_general(y_actual)
            else:
                # En páginas adicionales, solo dejar espacio para el título de la tabla
                y_actual -= 30
            
            # Dibujar títulos de la tabla de mercancías
            titulo_y = y_actual
            ancho_total = width - 52 
            PDFUtilidades.dibujar_celda_con_borde(
                p,
                30,
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
            
            # Determinar qué detalles mostrar en esta página - LOGICA CORREGIDA
            if mostrar_tabla_vacia_primera_pagina:
                if pagina == 0:
                    # PRIMERA PÁGINA: mostrar tabla VACÍA (más de 5 detalles)
                    detalles_pagina = []
                    dibujar_vacia = True
                else:
                    # PÁGINAS ADICIONALES: mostrar todos los detalles
                    inicio = (pagina - 1) * max_filas_paginas_adicionales
                    fin = min(inicio + max_filas_paginas_adicionales, total_detalles)
                    detalles_pagina = list(detalles_despacho[inicio:fin])
                    dibujar_vacia = False
            else:
                # Si hay 5 o menos detalles, mostrar todo en primera página
                if pagina == 0:
                    detalles_pagina = list(detalles_despacho)
                    dibujar_vacia = (len(detalles_pagina) == 0)
                else:
                    # No debería haber páginas adicionales en este caso
                    detalles_pagina = []
                    dibujar_vacia = False
            
            # Dibujar la tabla de mercancías
            y_despues_tabla = dibujar_tabla_mercancias(titulo_y - 20, detalles_pagina, dibujar_vacia, pagina > 0)
            
            # En la primera página, dibujar la información final después de la tabla
            if pagina == 0:
                y_despues_tabla = dibujar_informacion_final(y_despues_tabla)
            
            # Crear nueva página si es necesario
            if pagina < paginas_necesarias - 1:
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