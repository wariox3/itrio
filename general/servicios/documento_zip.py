from general.models.archivo import GenArchivo
from utilidades.utilidades import Utilidades
from utilidades.backblaze import Backblaze
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento_tipo import GenDocumentoTipo
from general.models.documento_impuesto import GenDocumentoImpuesto
import xml.etree.ElementTree as ET
from django.utils import timezone
from datetime import datetime, timedelta, date
import io
import zipfile

class DocumentoZipServicio():

    @staticmethod
    def datos(zip_data):                                                           
        zip_buffer = io.BytesIO(zip_data)            
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            xml_files = [f for f in zip_ref.namelist() if f.lower().endswith('.xml')]                
            if xml_files:                    
                if len(xml_files) <= 1:                    
                    xml_filename = xml_files[0]
                    with zip_ref.open(xml_filename) as xml_file:
                        xml_content = xml_file.read()
                        root = ET.fromstring(xml_content)
                        contacto = {
                            'numero_identificacion': '',
                            'nombre_corto': '',
                            'existe': False,
                            'contacto_id': None,
                            'ciudad': None,
                            'ciudad_id': None,
                            'ciudad_nombre': None,
                            'correo': None,
                            'plazo_pago_id': None
                        }
                        documento = {
                            'numero': '',
                            'prefijo': '',
                            'cue': '',
                            'fecha': '',
                            'fecha_vence': '',
                            'comentario' : '',
                            'detalles':[]
                        }
                        namespaces = {
                            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                        } 

                        description = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespaces=namespaces)
                        if description is not None and description.text:
                            cdata_content = description.text.strip()
                            if cdata_content.startswith('<![CDATA['):
                                cdata_content = cdata_content[9:-3]
                            inner_root = ET.fromstring(cdata_content)
                            inner_namespaces = {
                                'sts': 'dian:gov:co:facturaelectronica:Structures-2-1',
                                'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                                'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                            }
                            
                            contacto['numero_identificacion'] = inner_root.findtext('.//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID', namespaces=inner_namespaces)                            
                            contacto['nombre_corto'] = inner_root.findtext('.//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:RegistrationName', namespaces=inner_namespaces)                                                                                    
                            contacto['direccion'] = inner_root.findtext('.//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:RegistrationAddress/cac:AddressLine/cbc:Line', namespaces=inner_namespaces)
                            contacto['ciudad'] = inner_root.findtext('.//cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cac:RegistrationAddress/cbc:ID', namespaces=inner_namespaces)
                            if contacto['numero_identificacion']:
                                contacto_local = GenContacto.objects.filter(numero_identificacion = contacto['numero_identificacion']).first()
                                if contacto_local:
                                    contacto['existe'] = True
                                    contacto['contacto_id'] = contacto_local.id
                                    contacto['plazo_pago_id'] = contacto_local.plazo_pago_id
                                    contacto['correo'] = contacto_local.correo_electronico
                            if contacto['ciudad']:
                                ciudad = GenCiudad.objects.filter(codigo=contacto['ciudad']).first()
                                if ciudad:
                                    contacto['ciudad_id'] = ciudad.id
                                    contacto['ciudad_nombre'] = f"{ciudad.nombre} - {ciudad.estado.nombre}"             

                            documento['cue'] = inner_root.findtext('.//cbc:UUID', namespaces=inner_namespaces)
                            documento['prefijo'] = inner_root.findtext('.//sts:Prefix', namespaces=inner_namespaces)                                
                            numero = inner_root.findtext('.//cbc:ID', namespaces=inner_namespaces)
                            if documento['prefijo'] and numero.startswith(documento['prefijo']):
                                documento['numero'] = numero.replace(documento['prefijo'], '')
                            else:
                                documento['numero'] = numero                                                
                            documento['comentario'] = inner_root.findtext('.//cbc:Note', namespaces=inner_namespaces)
                            documento['fecha'] = inner_root.findtext('.//cbc:IssueDate', namespaces=inner_namespaces)
                            documento['fecha_vence'] = inner_root.findtext('.//cbc:PaymentDueDate', namespaces=inner_namespaces)                                                                                            
                            detalles=[]
                            lineas = inner_root.findall('.//cac:InvoiceLine', namespaces=inner_namespaces)                            
                            for linea in lineas:
                                detalle = {
                                    'item': linea.findtext('cbc:ID', namespaces=inner_namespaces),
                                    'item_nombre': linea.findtext('.//cac:Item/cbc:Description', namespaces=inner_namespaces),
                                    'cantidad': linea.findtext('cbc:InvoicedQuantity', namespaces=inner_namespaces),
                                    'precio_unitario': linea.findtext('.//cac:Price/cbc:PriceAmount', namespaces=inner_namespaces),
                                    'valor_total': linea.findtext('cbc:LineExtensionAmount', namespaces=inner_namespaces)
                                }
                                detalles.append(detalle)
                            documento['detalles'] = detalles

                        return {'error': False, 'documento':documento, 'contacto':contacto}
                else:
                    return {'error': True, 'mensaje': 'El ZIP contiene múltiples archivos XML'}
            else:
                return {'error':True , 'mensaje': 'El ZIP no contiene archivos XML'}
    
