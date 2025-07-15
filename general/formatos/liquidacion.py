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
        estilo_helvetica = ParagraphStyle(name='HelveticaStyle', fontName='Helvetica', fontSize=8, leading=8)   

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

            x = 24

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

            #empleado
            empleado_identificacion = ""
            liquidacion_dias = liquidacion.dias or 0
            if liquidacion.contrato:
                    contrato_fecha_ingreso = liquidacion.contrato.fecha_desde or ""
                    contrato_fecha_terminacion = liquidacion.contrato.fecha_hasta or ""
                    contrato_ciudad = liquidacion.contrato.ciudad_contrato.nombre or ""
                    contrato_salario = liquidacion.contrato.salario or 0
                    if liquidacion.contrato.contacto:
                        empleado_identificacion = liquidacion.contrato.contacto.numero_identificacion or ""
                        empleado_nombre = liquidacion.contrato.contacto.nombre_corto or ""
                        empleado_celular = liquidacion.contrato.contacto.celular or ""
                        empleado_banco = liquidacion.contrato.contacto.banco.nombre or ""
                        empleado_cuenta = liquidacion.contrato.contacto.numero_cuenta or ""
                        empleado_correo = liquidacion.contrato.contacto.correo or ""

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
            p.drawString(x, 610, "CELULAR: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 80, 610, str(empleado_celular))

            #Segunda columna
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 220, 650, "CIUDAD: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 260, 650, str(contrato_ciudad.upper()))      

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 220, 640, "BANCO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 260, 640, str(empleado_banco.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 220, 630, "CUENTA: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 260, 630, str(empleado_cuenta.upper()))

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 220, 620, "CORREO: ")
            p.setFont("Helvetica", 8)
            p.drawString(x + 260, 620, str(empleado_correo.upper()))

            #Tercer columna
            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 360, 650, "DÍAS LABORADOS: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 480, 650, f"{liquidacion_dias:,.0f}")        

            p.setFont("Helvetica-Bold", 8)
            p.drawString(x + 360, 640, "SALARIO: ")
            p.setFont("Helvetica", 8)
            p.drawRightString(x + 480, 640, f"{contrato_salario:,.0f}")     

        dibujar_encabezado()

        p.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes