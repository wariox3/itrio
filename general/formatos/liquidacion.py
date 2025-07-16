from general.models.empresa import GenEmpresa
from humano.models.liquidacion import HumLiquidacion
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from decouple import config

class FormatoLiquidacion():

    def generar_pdf(self, id):  
        buffer = BytesIO()   
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setTitle("liquidación")
        empresa = GenEmpresa.objects.filter(pk=1).first()
        liquidacion = HumLiquidacion.objects.select_related(
            'contrato',           
            'contrato__contacto',
            'contrato__contacto__ciudad' 
        ).filter(id=id).first()
        left_margin = 20
        right_margin = 20
        page_width = letter[0]
        usable_width = page_width - left_margin - right_margin

        def dibujar_encabezado():
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

            x = 20

            y = 680

            tamano_cuadrado = 1 * inch

            p.drawImage(logo, x, y, width=tamano_cuadrado, height=tamano_cuadrado, mask='auto')

            numero_identificacion = empresa.numero_identificacion or ""
            if hasattr(empresa, 'digito_verificacion') and empresa.digito_verificacion:
                numero_identificacion += f"-{empresa.digito_verificacion}"
            
            direccion = empresa.direccion or ""
            if empresa.ciudad and hasattr(empresa.ciudad, 'nombre'):
                direccion += f" - {empresa.ciudad.nombre.upper()}" if direccion else empresa.ciudad.nombre.upper()
            
            tipo_persona = f" - PERSONA {empresa.tipo_persona.nombre.upper()}" if (empresa.tipo_persona and hasattr(empresa.tipo_persona, 'nombre')) else ""
            
            p.setFont("Helvetica-Bold", 12)
            p.drawCentredString(x + 290, 745, "LIQUIDACIÓN")
            p.setFont("Helvetica-Bold", 9)
            p.drawString(x + 75, 735, empresa.nombre_corto.upper() if empresa.nombre_corto else "")
            p.setFont("Helvetica", 8)
            p.drawString(x + 75, 725, f"NIT: {numero_identificacion}{tipo_persona}")
            p.drawString(x + 75, 715, f"DIRECCIÓN: {direccion}")
            p.drawString(x + 75, 705, f"TEL: {empresa.telefono}" if empresa.telefono else "")

            liquidacion_comentario = str(liquidacion.comentario or "")
            liquidacion_dias = liquidacion.dias or 0

            if liquidacion.contrato:
                contrato = liquidacion.contrato
                contrato_fecha_ingreso = str(contrato.fecha_desde or "")
                contrato_fecha_terminacion = str(contrato.fecha_hasta or "")
                contrato_ciudad = str(contrato.ciudad_contrato.nombre if contrato.ciudad_contrato else "")
                contrato_salario = contrato.salario or 0
                contrato_grupo = str(contrato.grupo.nombre if contrato.grupo else "")
                
                if contrato.contacto:
                    contacto = contrato.contacto
                    empleado_identificacion = str(contacto.numero_identificacion or "")
                    empleado_nombre = str(contacto.nombre_corto or "")
                    empleado_celular = str(contacto.celular or "")
                    empleado_banco = str(contacto.banco.nombre if contacto.banco else "")
                    empleado_cuenta = str(contacto.numero_cuenta or "")
                    empleado_correo = str(contacto.correo or "")

            #Primer columna
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 650, "IDENTIFICACIÓN: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 650, str(empleado_identificacion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 640, "EMPLEADO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 640, str(empleado_nombre))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 630, "FECHA INGRESO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 630, str(contrato_fecha_ingreso))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 620, "FECHA RETIRO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 620, str(contrato_fecha_terminacion))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 610, "CORREO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 610, str(empleado_correo.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x, 600, "COMENTARIO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 600, str(liquidacion_comentario.upper()))


            #Segunda columna
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 280, 650, "CIUDAD: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 330, 650, str(contrato_ciudad.upper()))      

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 280, 640, "BANCO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 330, 640, str(empleado_banco.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 280, 630, "CUENTA: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 330, 630, str(empleado_cuenta.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 280, 620, "GRUPO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 330, 620, str(contrato_grupo.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 280, 610, "CELULAR: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 330, 610, str(empleado_celular))            

            #Tercer columna
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 420, 650, "DÍAS LABORADOS: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 550, 650, f"{liquidacion_dias:,.0f}")        

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 420, 640, "SALARIO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 550, 640, f"{contrato_salario:,.0f}")   
              
        def dibujar_cuerpo():
            x = 20
            y_position = 570
            
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 300, y_position, "DÍAS ")
            p.drawString(x + 380, y_position, "BASE ")
            p.drawString(x + 430, y_position, "ULTIMO PAGO ")
            p.drawString(x + 525, y_position, "TOTAL ")
            y_position -= 20

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 200, y_position, "CESANTÍAS")
            p.setFont("Helvetica", 9)
            p.drawRightString(x + 320, y_position, f"{liquidacion.dias_cesantia:,.0f}")
            p.drawRightString(x + 400, y_position, f"{liquidacion.salario:,.0f}")
            p.drawRightString(x + 485, y_position, str(liquidacion.fecha_ultimo_pago_cesantia))       
            p.drawRightString(x + 551, y_position, f"{liquidacion.cesantia:,.0f}")     
            y_position -= 20

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 200, y_position, "INTERESES:")
            p.setFont("Helvetica", 9)
            p.drawRightString(x + 320, y_position, f"{liquidacion.dias_cesantia:,.0f}")
            p.drawRightString(x + 400, y_position, f"{liquidacion.salario:,.0f}")
            p.drawRightString(x + 485, y_position, str(liquidacion.fecha_ultimo_pago_cesantia))       
            p.drawRightString(x + 551, y_position, f"{liquidacion.interes:,.0f}")     
            y_position -= 20

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 200, y_position, "PRIMA:")
            p.setFont("Helvetica", 9)
            p.drawRightString(x + 320, y_position, f"{liquidacion.dias_prima:,.0f}")
            p.drawRightString(x + 400, y_position, f"{liquidacion.salario:,.0f}")
            p.drawRightString(x + 485, y_position, str(liquidacion.fecha_ultimo_pago_prima))       
            p.drawRightString(x + 551, y_position, f"{liquidacion.prima:,.0f}")     
            y_position -= 20

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 200, y_position, "VACACIONES:")
            p.setFont("Helvetica", 9)
            p.drawRightString(x + 320, y_position, f"{liquidacion.dias_vacacion:,.0f}")
            p.drawRightString(x + 400, y_position, f"{liquidacion.salario:,.0f}")
            p.drawRightString(x + 485, y_position, str(liquidacion.fecha_ultimo_pago_vacacion))       
            p.drawRightString(x + 551, y_position, f"{liquidacion.vacacion:,.0f}")     
            y_position -= 20

        dibujar_encabezado()
        dibujar_cuerpo()

        p.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes