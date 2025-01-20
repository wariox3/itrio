from humano.models.programacion import HumProgramacion
from humano.models.programacion_detalle import HumProgramacionDetalle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from general.formatos.encabezado import FormatoEncabezado
from utilidades.utilidades import Utilidades
from reportlab.lib.colors import black, white, grey

class FormatoProgramacion():
    def __init__(self):
        self.encabezado = FormatoEncabezado()

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)                
        self.encabezado.generar_pdf(p, "PROGRAMACION DE NÓMINA")
        p.setFont("Helvetica", 10)        
        programacion = HumProgramacion.objects.filter(pk=id).values(
            'id', 'nombre', 'devengado', 'deduccion', 'total', 'fecha_desde', 'fecha_hasta'
            ).first()        
        programacion_detalles = HumProgramacionDetalle.objects.filter(programacion_id = id).values(
            'devengado', 'deduccion', 'total',
            'contrato__contacto__numero_identificacion',
            'contrato__contacto__nombre_corto',
            'contrato__contacto__numero_cuenta',
            'contrato__contacto__banco__nombre',
            ).order_by('-contrato__contacto__nombre_corto')

        x = 40
        y = 680
        alto_fila = 15  
        tamano_texto_encabezado = 9   
        p.setFont("Helvetica-Bold", tamano_texto_encabezado)    
        p.drawString(40, y - alto_fila * 1, 'CODIGO')
        p.drawString(40, y - alto_fila * 2, 'DESDE')
        p.drawString(40, y - alto_fila * 3, 'HASTA')
        p.drawString(40, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(110, y - alto_fila * 1, str(programacion['id']))
        p.drawString(110, y - alto_fila * 2, programacion['fecha_desde'].strftime('%Y-%m-%d'))
        p.drawString(110, y - alto_fila * 3, programacion['fecha_hasta'].strftime('%Y-%m-%d'))
        p.drawString(110, y - alto_fila * 4, '')    

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(270, y - alto_fila * 1, 'NOMBRE')
        p.drawString(270, y - alto_fila * 2, '')
        p.drawString(270, y - alto_fila * 3, '')
        p.drawString(270, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(320, y - alto_fila * 1, Utilidades.pdf_texto(programacion['nombre'], 30))
        p.drawString(320, y - alto_fila * 2, '')
        p.drawString(320, y - alto_fila * 3, '')
        p.drawString(320, y - alto_fila * 4, '')  

        p.setFont("Helvetica-Bold", tamano_texto_encabezado) 
        p.drawString(460, y - alto_fila * 1, 'DEVENGADO')
        p.drawString(460, y - alto_fila * 2, 'DEDUCCION')
        p.drawString(460, y - alto_fila * 3, 'TOTAL')
        p.drawString(460, y - alto_fila * 4, '')
        p.setFont("Helvetica", tamano_texto_encabezado)
        p.drawString(520, y - alto_fila * 1, f"{programacion['devengado']:,.0f}")
        p.drawString(520, y - alto_fila * 2, f"{programacion['deduccion']:,.0f}")
        p.drawString(520, y - alto_fila * 3, f"{programacion['total']:,.0f}")
        p.drawString(520, y - alto_fila * 4, '')         

        y = 580
        margen = 2
        ancho_columna = [220, 70, 60, 60, 60, 60]  # Ajuste de anchos para combinar identificación y empleado

        # Dibujar encabezados

        p.setFont("Helvetica-Bold", 8)
        p.setFillColor(grey)  # Fondo gris para los encabezados
        p.rect(x, y, sum(ancho_columna), alto_fila, fill=True, stroke=False)  # Rellenar fondo de encabezados
        p.setFillColor(white)  # Texto blanco

        # Dibujar texto de encabezados
        p.drawString(x + sum(ancho_columna[:0]) + margen, y + 4, 'IDENTIFICACIÓN - EMPLEADO')
        p.drawString(x + sum(ancho_columna[:1]) + margen, y + 4, 'CUENTA')            
        p.drawString(x + sum(ancho_columna[:2]) + margen, y + 4, 'BANCO')
        p.drawString(x + sum(ancho_columna[:3]) + margen, y + 4, 'DEVENGADO')
        p.drawString(x + sum(ancho_columna[:4]) + margen, y + 4, 'DEDUCCIÓN')
        p.drawString(x + sum(ancho_columna[:5]) + margen, y + 4, 'TOTAL')

        # Dibujar bordes de la tabla (encabezados)
        p.setFillColor(grey)  # Fondo gris para los encabezados
        p.rect(x, y, sum(ancho_columna), alto_fila, fill=True, stroke=False)  # Rellenar fondo de encabezados
        p.setFillColor(white)  # Texto blanco para encabezados

        # Dibujar texto de encabezados
        p.setFont("Helvetica-Bold", 8)
        p.drawString(x + sum(ancho_columna[:0]) + margen, y + 4, 'IDENTIFICACIÓN - EMPLEADO')
        p.drawString(x + sum(ancho_columna[:1]) + margen, y + 4, 'CUENTA')            
        p.drawString(x + sum(ancho_columna[:2]) + margen, y + 4, 'BANCO')
        p.drawString(x + sum(ancho_columna[:3]) + margen, y + 4, 'DEVENGADO')
        p.drawString(x + sum(ancho_columna[:4]) + margen, y + 4, 'DEDUCCIÓN')
        p.drawString(x + sum(ancho_columna[:5]) + margen, y + 4, 'TOTAL')

        # Dibujar bordes de las celdas (encabezados)
        for i in range(6):
            p.setStrokeColor(black)
            p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila, fill=False, stroke=True)

        y -= alto_fila  # Mover hacia abajo para las filas de contenido

        # Contenido de la tabla
        p.setFont("Helvetica", 8)
        for index, programacion_detalle in enumerate(programacion_detalles):  # Usar enumerate para obtener el índice
            y_texto = y + 5

            p.setFillColor(white)  # Fondo blanco
            p.setFillColor(black)  # Texto negro

            # Dibujar contenido
            identificacion_empleado = f"{programacion_detalle.get('contrato__contacto__numero_identificacion', '')} - {programacion_detalle.get('contrato__contacto__nombre_corto', '')[:30]}"
            p.drawString(x + sum(ancho_columna[:0]) + margen, y_texto, identificacion_empleado)
            p.drawString(x + sum(ancho_columna[:1]) + margen, y_texto, str(programacion_detalle.get('contrato__contacto__numero_cuenta', "") or ""))
            p.drawString(x + sum(ancho_columna[:2]) + margen, y_texto, str(programacion_detalle.get('contrato__contacto__banco__nombre', "") or ""))                        
            p.drawRightString(x + sum(ancho_columna[:3]) + ancho_columna[3] - margen, y_texto, f"{programacion_detalle.get('devengado', 0):,.0f}")
            p.drawRightString(x + sum(ancho_columna[:4]) + ancho_columna[4] - margen, y_texto, f"{programacion_detalle.get('deduccion', 0):,.0f}")
            p.drawRightString(x + sum(ancho_columna[:5]) + ancho_columna[5] - margen, y_texto, f"{programacion_detalle.get('total', 0):,.0f}")

            # Dibujar bordes de las celdas
            for i in range(6):
                p.rect(x + sum(ancho_columna[:i]), y, ancho_columna[i], alto_fila, fill=False, stroke=True)
            
            y -= alto_fila  # Mover hacia abajo para la siguiente fila


        p.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
