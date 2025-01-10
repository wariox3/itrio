from num2words import num2words
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
import re
import string

def convertir_a_letras(numero):
    if numero == 0:
        return "Cero pesos"
    
    if numero < 0 or numero >= 1000000000:
        return "Número fuera de rango"
    
    palabras = num2words(numero, lang='es').title()
    
    # Reemplazar "Y Un" por "Y Unos" cuando corresponda
    palabras = palabras.replace("Y Un ", "Y Unos ")
    
    # Agregar "Pesos" al final
    palabras += " Pesos"
    
    return palabras.upper()

def generar_qr(data):
    qr_code = QrCodeWidget(data)
    d = Drawing(45, 45)
    d.add(qr_code)
    return d

class Utilidades:
    @staticmethod
    def rellenar(cadena, largo, caracter, direccion = "I"):
        if not isinstance(cadena, str):
            cadena = str(cadena)
        if not cadena:
            cadena = ""
        longitud = len(cadena)
        if longitud < largo:
            if direccion == "I":
                cadena = caracter * (largo - longitud) + cadena
            else:
                cadena = cadena + caracter * (largo - longitud)
        else:
            cadena = cadena[:largo]        
        return cadena    
        
    @staticmethod
    def eliminar_caracteres_especiales(cadena):
        return re.sub(r'[^a-zA-Z0-9\s]', '', cadena)  
             
    @staticmethod
    def correo_valido(correo):
        try:
            validate_email(correo)
            return True
        except ValidationError:
            return False    
        
    @staticmethod    
    def dias_prestacionales(fecha_inicio, fecha_fin):
        """
        Calcula el número de días entre dos fechas suponiendo meses de 30 días.

        :param fecha_inicio: Fecha inicial en formato 'YYYY-MM-DD'.
        :param fecha_fin: Fecha final en formato 'YYYY-MM-DD'.
        :return: Número de días entre las dos fechas, con meses de 30 días.
        """
        # Convertimos las fechas en objetos datetime
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        # Calculamos las diferencias de años, meses y días
        años = fin.year - inicio.year
        meses = fin.month - inicio.month
        dias = fin.day - inicio.day

        # Totalizamos los meses y los días
        total_meses = años * 12 + meses
        total_dias = total_meses * 30 + dias
        total_dias += 1
        return total_dias
    
    @staticmethod
    def digito_verificacion(nit):
        factores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
        #rut_ajustado=string.rjust(str(nit), 15, '0')
        rut_ajustado=str(nit).rjust( 15, '0')
        s = sum(int(rut_ajustado[14-i]) * factores[i] for i in range(14)) % 11
        if s > 1:
            return 11 - s
        else:
            return s                 