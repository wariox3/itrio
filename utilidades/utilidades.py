def convertir_a_letras(numero):
    unidades = ["", "UN", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    especiales = ["", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"]
    decenas = ["", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"]
    centenas = ["", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]

    miles = ["", "MIL", "MILLÓN", "MIL MILLONES", "BILLÓN", "MIL BILLONES", "TRILLÓN"]

    if numero == 0:
        return "CERO"

    letras = ""
    if numero < 0:
        letras += "MENOS "
        numero = abs(numero)

    i = 0
    while numero > 0:
        grupo = numero % 1000
        if grupo != 0:
            letras_grupo = ""
            centena = grupo // 100
            decena = (grupo % 100) // 10
            unidad = grupo % 10

            if centena > 0:
                letras_grupo += centenas[centena] + " "

            if decena == 1:
                letras_grupo += especiales[unidad]
            else:
                if decena > 1:
                    letras_grupo += decenas[decena]
                if unidad > 0:
                    if decena >= 2:
                        letras_grupo += " Y "
                    letras_grupo += unidades[unidad]

            letras = letras_grupo + miles[i] + " " + letras

        numero //= 1000
        i += 1

    letras = letras.strip()
    if letras.endswith("MIL"):
        letras = letras.replace("MIL", "MIL ")
    letras += " PESOS"
    return letras.strip()


