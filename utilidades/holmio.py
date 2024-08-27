from general.models.complemento import GenComplemento
from decouple import config
import requests
import json
from requests.auth import HTTPBasicAuth

class Holmio():

    def ruteoPendiente(self, parametros):
        url = "/api/transporte/guia/ruteo/pendiente"        
        respuesta = self.consumirPost(parametros, url)        
        if respuesta['status'] == 200:
            datos = respuesta['datos']
            return {'error':False, 'guias': datos['guias']}
        else:
            return {'error':True, 'mensaje':f'Ocurrio un error con la clase: {respuesta["mensaje"]}'}

    def ruteoMarcar(self, parametros):
        url = "/api/transporte/guia/ruteo/marcar"        
        respuesta = self.consumirPost(parametros, url)        
        if respuesta['status'] == 200:
            return {'error':False}
        else:
            return {'error':True, 'mensaje':f'Ocurrio un error con la clase: {respuesta["mensaje"]}'}

    def consumirPost(self, data, url):
        complemento = GenComplemento.objects.get(pk=1)
        if complemento:
            if isinstance(complemento.datos_json, list):
                    config_dict = {item['nombre']: item['valor'] for item in complemento.datos_json}
                    url_base = config_dict.get('url')
                    usuario = config_dict.get('usuario')
                    clave = config_dict.get('clave')                
                    if url_base and usuario and clave:  
                        url_completa = url_base + url    
                        json_data = json.dumps(data)
                        headers = {'Content-Type': 'application/json'}
                        response = requests.post(
                            url_completa,
                            data=json_data,
                            headers=headers,
                            auth=HTTPBasicAuth(usuario, clave)
                        )                        
                        resp = response.json()
                        return {'status': response.status_code, 'datos': resp}
                    else:
                        return {'status': 500, 'mensaje': 'Debe configurar los datos del complemento'}    
                
            else:
                return {'status': 500, 'mensaje': 'El complemento no tiene json valido'}
        else:
            return {'status': 500, 'mensaje': 'El complemento no existe'}




