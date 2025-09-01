from general.models.archivo import GenArchivo
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from general.models.documento import GenDocumento
import requests
import json
import hashlib

class DocumentoServicio():

    @staticmethod
    def generar_cufe(documento: GenDocumento):                                                   
        
        emisor_numero_identificacion = '901192048'
        adquiriente_numero_identificacion = documento.contacto.numero_identificacion
        numero_completo = documento.numero
        if documento.resolucion:
            numero_completo = f'{documento.resolucion.prefijo}{documento.numero}'

        
        fecha_factura = ''
        hora_factura = ''
        subtotal = ''
        iva = ''
        consumo = ''
        ica = ''
        total = ''
        clave_tecnica = ''
        ambiente = '1'
        cufe = f'{numero_completo}{fecha_factura}{hora_factura}{subtotal}01{iva}04{consumo}03{ica}{total}{emisor_numero_identificacion}{adquiriente_numero_identificacion}{clave_tecnica}{ambiente}'
        UUID = hashlib.sha384(cufe.encode()).hexdigest()

        return UUID                          