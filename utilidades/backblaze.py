from b2sdk.v2 import InMemoryAccountInfo, B2Api, UploadSourceBytes
import requests
import json

class Backblaze():

    def __init__(self, app_key_id, app_key):        
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        self.b2_api.authorize_account("production", app_key_id, app_key)


    def log_correo(self, operador, documento_id):
        url = "/api/externo/correo/v2"
        datos = {
            "operador" : operador,
            "codigoDocumento" : documento_id
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            datos = respuesta['datos']
            return {'error': False, 'correos': datos['correos']}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio zinc'}    


