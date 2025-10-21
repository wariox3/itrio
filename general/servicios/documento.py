from general.models.archivo import GenArchivo
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_tipo import GenDocumentoTipo
from general.models.documento_impuesto import GenDocumentoImpuesto
import requests
import json
import hashlib
from django.utils import timezone
from datetime import datetime, timedelta, date

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
    
    @staticmethod
    def generar_recurrente(documento_ids: list):
        documentos_creados = []
        documentos = GenDocumento.objects.filter(id__in=documento_ids)
        if not documentos.exists():
            return {'error': True, 'mensaje': 'No se encontraron documentos para procesar'}
        for documento in documentos:
            if documento.documento_tipo_id in [16, 32]:
                documento_tipo_id = None
                if documento.documento_tipo_id == 16:
                    documento_tipo_id = 1
                if documento.documento_tipo_id == 32:
                    documento_tipo_id = 5
                if documento_tipo_id:
                    
                    documento_tipo = GenDocumentoTipo.objects.get(id=documento_tipo_id)
                    dias_plazo = documento.plazo_pago.dias
                    documento_data = documento.__dict__.copy()
                    documento_data.pop('id', None)           
                    documento_data.pop('_state', None)
                    documento_data['documento_tipo_id'] = documento_tipo_id
                    documento_data['resolucion_id'] = documento_tipo.resolucion_id
                    documento_data['fecha'] = timezone.now()
                    documento_data['fecha_contable'] = timezone.now()
                    documento_data['fecha_vence'] = timezone.now() + timedelta(days=dias_plazo)
                    
                    documento_nuevo = GenDocumento(**documento_data)
                    documento_nuevo.save()
                    documentos_creados.append(documento_nuevo.id)
                    
                    documento_detalles = GenDocumentoDetalle.objects.filter(documento_id=documento.id).order_by('id')
                    for documento_detalle in documento_detalles:
                        documento_detalle_data = documento_detalle.__dict__.copy()
                        documento_detalle_data.pop('id', None)
                        documento_detalle_data.pop('_state', None)
                        documento_detalle_data['documento_id'] = documento_nuevo.id
                        
                        documento_detalle_nuevo = GenDocumentoDetalle(**documento_detalle_data)
                        documento_detalle_nuevo.save()
                        
                        documento_impuestos = GenDocumentoImpuesto.objects.filter(documento_detalle_id=documento_detalle.id)
                        for documento_impuesto in documento_impuestos:
                            documento_impuesto_data = documento_impuesto.__dict__.copy()
                            documento_impuesto_data.pop('id', None)
                            documento_impuesto_data.pop('_state', None)
                            documento_impuesto_data['documento_detalle_id'] = documento_detalle_nuevo.id
                            
                            documento_impuesto_nuevo = GenDocumentoImpuesto(**documento_impuesto_data)
                            documento_impuesto_nuevo.save()
            else:
                return {'error': True, 'mensaje': f'El documento con id {documento.id} no es recurrente'}
        return {'error': False, 'documentos_creados': documentos_creados}