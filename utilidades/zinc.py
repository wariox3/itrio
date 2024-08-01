from general.models.empresa import GenEmpresa
from general.models.documento_tipo import GenDocumentoTipo
from general.models.resolucion import GenResolucion
import requests
import json

class Zinc():

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

    def log_evento(self, operador, documento_id):
        url = "/api/externo/evento/v3"
        datos = {
            "operador" : operador,
            "codigoDocumento" : documento_id
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            datos = respuesta['datos']
            return {'error': False, 'eventos': datos['eventos']}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio zinc'}

    def log_envio(self, operador, documento_id):
        url = "/api/externo/log_envio"
        datos = {
            "operador" : operador,
            "codigoDocumento" : documento_id
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            datos = respuesta['datos']
            return {'error': False, 'log': datos['log']}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio zinc'}

    def decodificar_direccion(self, direcciones):
        url = "/api/mapa/decodificar"
        datos = {
            "cuenta": "1",
            "modelo": "guia",
            "canal": 3,
            "direcciones": direcciones
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            datos = respuesta['datos']
            return {'error': False, 'direcciones': datos['direcciones']}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio zinc'}

    def correo_reddoc(self, correo, asunto, contenido):
        url = "/api/correo/reddoc"
        datos = {
            "correo" : correo,
            "asunto" : asunto,
            "contenido": contenido
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            return {'error': False}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio zinc'}

    def consumirPost(self, data, url):
        url = "http://zinc.semantica.com.co" + url
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        resp = response.json()
        return {'status': response.status_code, 'datos': resp}


