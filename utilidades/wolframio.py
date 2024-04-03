from general.models.empresa import Empresa
from general.models.documento_tipo import DocumentoTipo
import requests
import json

class Wolframio():

    def activarCuenta(self, setPruebas):        
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
        self.consumirPost(datos, url)        
        '''documentoTipo = DocumentoTipo.objects.get(pk=1)
        if 'id' in respuesta:
            rededoc_id = respuesta.get('id')
            if empresa.rededoc_id is None or empresa.rededoc_id == '':
                resolucion = Resolucion.objects.get(pk=resolucion_id)
                documentoTipo.resolucion = resolucion
                empresa.rededoc_id = rededoc_id
                documentoTipo.save()
                empresa.save()
            else:
                return Response({'mensaje': 'La empresa ya se encuentra activa', 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            validacion = respuesta.get('validacion')
            return Response({'mensaje': {validacion}, 'codigo': 15}, status=status.HTTP_400_BAD_REQUEST)'''
        return {'error':True, 'mensaje':'Un error desde wolframio'}
        
        

    def consumirPost(self, data, url):
        url = "http://159.203.18.130/wolframio/public/index.php" + url
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_data, headers=headers)
        resp = response.json()
        return resp


