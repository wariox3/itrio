from contenedor.models import CtnInformacionFacturacion
from decouple import config
import requests


class MovimientoServicio():

    @staticmethod
    def crear_factura(informacion_facturacion_id, valor):       
        try:
            if informacion_facturacion_id and valor:
                env = config('ENV', default='prod')
                if env == 'prod' or env == 'dev':                                     
                    contenedor = config('FACTURACION_CONTENEDOR')
                    url_base = "http://localhost:8000" if env == 'dev' else "https://reddocapi.co"    
                    url_base_contenedor = f"http://{contenedor}.localhost:8000" if env == 'dev' else f"https://{contenedor}.reddocapi.co"    
                    token =  MovimientoServicio.autenticar(url_base)
                    contacto_id = MovimientoServicio.contacto(url_base_contenedor, token, informacion_facturacion_id)                    
                    if contacto_id:                
                        headers = {
                            'Authorization': f'Bearer {token}',
                            'Content-Type': 'application/json'
                        } 
                        data = {
                            "empresa": 1,
                            "contacto": contacto_id,
                            "totalCantidad": 1,
                            "contactoNombre": "Consumidor final",
                            "numero": None,
                            "fecha": "2025-07-25",
                            "fecha_vence": "2025-07-25",
                            "forma_pago": None,
                            "forma_pago_nombre": "",
                            "metodo_pago": 1,
                            "metodo_pago_nombre": "",
                            "almacen": 1,
                            "almacen_nombre": "Principal",
                            "total": valor,
                            "subtotal": valor,
                            "base_impuesto": 0,
                            "impuesto": 0,
                            "impuesto_operado": 0,
                            "impuesto_retencion": 0,
                            "remision": None,
                            "afectado": 0,
                            "total_bruto": valor,
                            "comentario": None,
                            "orden_compra": None,
                            "documento_referencia": None,
                            "documento_referencia_numero": None,
                            "asesor": "",
                            "asesor_nombre_corto": None,
                            "sede": 1,
                            "resolucion": "",
                            "resolucion_numero": "",
                            "descuento": 0,
                            "sede_nombre": None,
                            "grupo_contabilidad": None,
                            "plazo_pago": 1,
                            "detalles": [
                                {
                                    "cuenta": None,
                                    "cuenta_codigo": None,
                                    "cuenta_nombre": None,
                                    "item": 1,
                                    "item_nombre": "SERVICIOS NUBE",
                                    "cantidad": 1,
                                    "precio": valor,
                                    "porcentaje_descuento": 0,
                                    "descuento": 0,
                                    "subtotal": valor,
                                    "total": valor,
                                    "impuesto": 0,
                                    "impuesto_operado": 0,
                                    "impuesto_retencion": 0,
                                    "total_bruto": valor,
                                    "neto": valor,
                                    "grupo": None,
                                    "base_impuesto": 0,
                                    "almacen": 1,
                                    "almacen_nombre": "Principal",
                                    "impuestos": [],
                                    "impuestos_eliminados": [],
                                    "id": None,
                                    "tipo_registro": "I",
                                    "naturaleza": None
                                }
                            ],
                            "pagos": [],
                            "referencia_cue": None,
                            "referencia_numero": None,
                            "referencia_prefijo": None,
                            "detalles_eliminados": [],
                            "pagos_eliminados": [],
                            "documento_tipo": 1
                        }                    
                        url = f"{url_base_contenedor}/general/documento/nuevo/"
                        respuesta = requests.post(
                            url,
                            json=data,
                            headers=headers,
                            timeout=10
                        )
                        if respuesta.ok:
                            respuesta_json = respuesta.json()
                            factura_id = respuesta_json['documento']['id']
                            return factura_id
                        else:
                            return None
                    else:
                        return None                        
                else:
                    return None
            else:
                return None
        except Exception as e:
            return None   
        
    def autenticar(url_base):
        try:
            url = f"{url_base}/seguridad/login/"
            usuario = config('FACTURACION_USUARIO')
            clave = config('FACTURACION_CLAVE')
            if usuario and clave:
                data = {
                    "username": usuario,
                    "password": clave
                }
                headers = {
                    "Content-Type": "application/json"
                }

                respuesta = requests.post(
                    url,
                    json=data,
                    headers=headers,
                    timeout=10
                )
                if not respuesta.ok:
                    return ""                        
                token = respuesta.json().get('token', '')        
                return token
            else:
                return ""
        except Exception as e:
            return ""  
        
    def contacto(url_base_contenedor, token, informacion_facturacion_id):
        try:
            informacion_facturacion = CtnInformacionFacturacion.objects.get(pk=informacion_facturacion_id)
            if not informacion_facturacion:
                return None

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }                
            data = {
                "identificacion_id" : informacion_facturacion.identificacion_id,
                "numero_identificacion" : informacion_facturacion.numero_identificacion
            }
            url = f"{url_base_contenedor}/general/contacto/validar/"
            respuesta = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=10
            )
            if respuesta.ok:          
                respuesta_json = respuesta.json()
                return respuesta_json.get('id')
            else:
                return None            
        except Exception as e:
            return None        
    
