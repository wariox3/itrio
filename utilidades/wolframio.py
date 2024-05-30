from general.models.empresa import Empresa
from general.models.documento_tipo import DocumentoTipo
from general.models.resolucion import Resolucion
import requests
import json

class Wolframio():

    def activarCuenta(self, set_pruebas, resolucion_id, correo_facturacion_electronica):        
        url = "/api/cuenta/nuevo"
        empresa = Empresa.objects.get(pk=1)
        datos = {
            "numeroIdentificacion" : empresa.numero_identificacion,
            "nombre" : empresa.nombre_corto,
            "celular" : empresa.telefono,
            "correo" : empresa.correo,
            "ciudadId" : empresa.ciudad_id,
            "identificacionId" : empresa.identificacion.id,
            "webhookEmision" : f"https://{empresa.subdominio}.reddocapi.co/general/documento/electronico_respuesta_emitir/",
            "webhookNotificacion" : f"https://{empresa.subdominio}.reddocapi.co/general/documento/electronico_respuesta_notificar/",
            "setPruebas" : set_pruebas,
            "correoFacturacionElectronica" : correo_facturacion_electronica
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
        
    def emitir(self, datos):
        url = "/api/documento/nuevo"
        respuesta = self.consumirPost(datos, url)    
        datos = respuesta['datos']
        if respuesta['status'] == 200:
            return {'error':False, 'id': datos['id']}
        elif respuesta['status'] == 500:
            detalle = datos.get('detail', "")
            return {'error':True, 'mensaje': f"Ocurrio un error grave en el servicio de wolframio notifique su proveedor del software y ayude a mejorar nuestro producto {detalle}"}
        else:
            return {'error':True, 'mensaje': datos['mensaje']}

    def notificar(self, documento_id, base64):
        url = "/api/documento/notificar"
        datos = {
            "documentoId" : documento_id,
            "facturaB64" : base64
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            return {'error': False}
        else:
            return {'error':True, 'mensaje':'Ocurrio un error en el servicio wolframio'}

    def renotificar(self, documento_id, correo):
        url = "/api/documento/renotificar"
        datos = {
            "documentoId" : documento_id,
            "correo" : correo
        }
        respuesta = self.consumirPost(datos, url)
        if respuesta['status'] == 200:
            return {'error': False}
        else:
            datos = respuesta['datos']
            return {'error':True, 'mensaje':f"Ocurrio un error en el servicio wolframio: {datos['mensaje']}"}

    def consumirPost(self, data, url):
        url = "http://159.203.18.130/wolframio/public/index.php" + url
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        resp = response.json()
        return {'status': response.status_code, 'datos': resp}


