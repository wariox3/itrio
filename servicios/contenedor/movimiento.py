from contenedor.models import CtnInformacionFacturacion
from decouple import config
import requests


class MovimientoServicio():

    @staticmethod
    def crear_factura(informacion_facturacion_id, valor):       
        try:
            env = config('ENV', default='prod')
            if env == 'prod':
                dominio_backend = config('DOMINIO_BACKEND')
                empresa_facturacion = config('EMPRESA_FACTURACION')

                # solo para pruebas localhost
                if dominio_backend == 'localhost':
                    dominio_backend = 'localhost:8000'

                protocolo = 'http' if env == 'prod' else 'http'

                base_url = f"{protocolo}://{dominio_backend}"

                auth_url = f"{base_url}/seguridad/login/"
                auth_data = {
                    "username": config('USUARIO_FACTURACION'),
                    "password": config('PASS_FACTURACION')
                }

                headers_api_interno = {
                    "X-Internal-Auth": config("AUT_INTERNA"),
                    "Content-Type": "application/json"
                }

                auth_response = requests.post(
                    auth_url,
                    json=auth_data,
                    headers=headers_api_interno,
                    timeout=10
                )
                auth_response.raise_for_status()
            
                auth_token = auth_response.json().get('token')

                headers = {
                    'Authorization': f'Bearer {auth_token}',
                    'Content-Type': 'application/json'
                }
            
                informacion_facturacion = CtnInformacionFacturacion.objects.filter(pk=informacion_facturacion_id).get()


                contacto_data = {
                    "identificacion_id" : informacion_facturacion.identificacion_id,
                    "numero_identificacion" : informacion_facturacion.numero_identificacion
                }

                base_url_empresa_facturacion = f"{protocolo}://{empresa_facturacion}.{dominio_backend}"

                api_url_consultar_contacto = f"{base_url_empresa_facturacion}/general/contacto/validar/"

                respuesta_contacto = requests.post(
                    api_url_consultar_contacto,
                    json=contacto_data,
                    headers=headers,
                    timeout=10
                )

                respuesta_contacto.raise_for_status()

                contacto_json = respuesta_contacto.json()

                contacto_id = contacto_json.get('id')

                factura_data = {
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

            
                api_url_empresa = f"{base_url_empresa_facturacion}/general/documento/nuevo/"

                respuesta_factura = requests.post(
                    api_url_empresa,
                    json=factura_data,
                    headers=headers,
                    timeout=10
                )

                respuesta_factura.raise_for_status()

                factura_json = respuesta_factura.json()

                factura_id = factura_json['documento']['id']

                if respuesta_factura.status_code == 200:
                    return factura_id
                else:
                    None
            else:
                None
        except Exception as api_error:
            return None          