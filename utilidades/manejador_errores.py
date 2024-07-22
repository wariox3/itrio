import logging
import requests
import json
from django.http import HttpRequest
from decouple import config

class WebServiceHandler(logging.Handler):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def emit(self, record):     
        if config('ENV') == 'prod' or config('ENV') == 'test':
            traza = self.format(record)   
            fuente = record.name     
            if fuente == 'django.request':
                ruta = ''
                usuario = ''
                request_info = getattr(record, 'request', None)
                if isinstance(request_info, HttpRequest):
                    ruta = request_info.path
                    usuario = str(request_info.user) if request_info.user.is_authenticated else 'anonymous'

                mensaje = ''
                if record.exc_info and hasattr(request_info, 'path'):
                    exc_type, exc_value, exc_traceback = record.exc_info
                    mensaje = f"{exc_value}"
                datos = {            
                    'mensaje': mensaje,
                    'archivo': record.pathname,
                    'ruta': ruta,
                    'usuario': usuario,
                    'traza': traza,
                    'entorno': config('ENV')
                }      
                json_data = json.dumps(datos)
                headers = {'Content-Type': 'application/json'}
                requests.post(self.url, data=json_data, headers=headers)
                