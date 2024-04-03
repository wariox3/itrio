from general.models.empresa import Empresa
from general.models.documento_tipo import DocumentoTipo
from general.models.resolucion import Resolucion
import requests
import json

class Wolframio():

    def activarCuenta(self, setPruebas, resolucion_id):        
        url = "/api/cuenta/nuevo"
        empresa = Empresa.objects.get(pk=1)
        datos = {
            "numeroIdentificacion" : empresa.numero_identificacion,
            "nombre" : empresa.nombre_corto,
            "celular" : empresa.telefono,
            "correo" : empresa.correo,
            "ciudadId" : empresa.ciudad_id,
            "identificacionId" : empresa.identificacion.id,
            "webhookEmision" : "webhookEmision",
            "webhookNotificacion" : "webhookNotificacion",
            "setPruebas" : setPruebas
        }
        respuesta = self.consumirPost(datos, url)        
        if respuesta['status'] == 200:
            datosRespuesta = respuesta['datos']            
            if empresa.rededoc_id is None or empresa.rededoc_id == '':
                documentoTipo = DocumentoTipo.objects.get(pk=1)
                resolucion = Resolucion.objects.get(pk=resolucion_id)
                documentoTipo.resolucion = resolucion
                empresa.rededoc_id = datosRespuesta['id']
                documentoTipo.save()
                empresa.save()
                return {'error':False}
            else:            
                return {'error':True, 'mensaje':'La empresa ya se encuentra activa'}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio wolframio'}

        
    def consumirPost(self, data, url):
        url = "http://159.203.18.130/wolframio/public/index.php" + url
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        resp = response.json()
        return {'status': response.status_code, 'datos': resp}


