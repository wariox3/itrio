from num2words import num2words

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


