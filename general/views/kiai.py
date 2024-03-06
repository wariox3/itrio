from django.http import JsonResponse
import requests
import json


def enviar_software_estrategico(data):
    em = data.get('em')
    
    proceso_factura_electronica = {
        'estado': 'NO',
        'codigoExterno': '',
        'cue': '',
        'cadenaCodigoQr': '',
        'correo': 'SI'
    }

    if data.get('dat_tipoAmbiente') == 1:
        url = "https://apps.kiai.co/api/ConValidacionPrevia/EmitirDocumento"
    else:
        url = "https://apps.kiai.co/api/ConValidacionPrevia/CrearSetPrueba"

    arr_software_estrategico = arr_kiai(data)
    json_data = json.dumps(arr_software_estrategico)

    headers = {'Content-Type': 'application/json'}
    auth = ("900395252", "tufactura.co@softwareestrategico.com")

    try:
        response = requests.post(url, data=json_data, headers=headers, auth=auth, timeout=20)

        # Verificar el estado de la respuesta
        response.raise_for_status()

        # Obtener la respuesta como JSON
        resp = response.json()

        if resp:
             if 'Message' in resp:
                 if 'ExceptionMessage' in resp:
                     datos = resp['ExceptionMessage']
        #             ar_respuesta = GenRespuestaFacturaElectronica()
        #             ar_respuesta.fecha = timezone.now()
        #             ar_respuesta.codigo_documento = data.get('doc_codigo')
        #             ar_respuesta.error_message = resp['ExceptionMessage']
        #             ar_respuesta.save()

        #         proceso_factura_electronica['estado'] = 'ER'

        #     if 'Validaciones' in resp:
        #         validaciones = resp['Validaciones']
        #         if validaciones['Valido']:
        #             proceso_factura_electronica['estado'] = 'EX'
        #             proceso_factura_electronica['codigoExterno'] = validaciones['DoceId']
        #             control = resp['Control']
        #             if control:
        #                 proceso_factura_electronica['cue'] = control['CufeCude']
        #                 proceso_factura_electronica['cadenaCodigoQr'] = control['CadenaCodigoQr']
        #         else:
        #             # ... Manejo de errores adicionales
        #             pass
        # else:
        #     proceso_factura_electronica['estado'] = 'ER'
        #     ar_respuesta = GenRespuestaFacturaElectronica()
        #     ar_respuesta.fecha = timezone.now()
        #     ar_respuesta.codigo_documento = data.get('doc_codigo')
        #     ar_respuesta.error_message = "Error servidor kiai"
        #     ar_respuesta.save()

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        proceso_factura_electronica['estado'] = 'ER'

    return JsonResponse(proceso_factura_electronica)


def arr_kiai(arr_factura):
    res_prefijo = str(arr_factura['res_prefijo']) or ""
    doc_numero = str(arr_factura['doc_numero']) or ""
    numero = res_prefijo + doc_numero
    tipo = '01'
    tipo_codigo = arr_factura['doc_tipo_operacion']
    fecha_vencimiento = str(arr_factura['doc_fecha_vence']) or ""
    hora = str(arr_factura['doc_hora2']) or ""
    forma_pago = 1
    if arr_factura['doc_formaPago'] == "CRE":
        forma_pago = 2
    if arr_factura['doc_tipo'] == 'NC':
        numero = arr_factura['doc_prefijo'] + arr_factura['doc_numero']
        tipo = '91'
        tipo_codigo = "20" if arr_factura['ref_codigoExterno'] else "22"
    if arr_factura['doc_tipo'] == 'ND':
        numero = arr_factura['doc_prefijo'] + arr_factura['doc_numero']
        tipo = '92'
        tipo_codigo = "30" if arr_factura['ref_codigoExterno'] else "32"

    arr_impuestos = []
    for item in arr_factura['doc_itemes']:
        arr_impuestos.append({
            "DediBase": item['item_base_iva'],
            "DediValor": item['item_iva'],
            "DediFactor": item['item_porcentaje_iva'],
            "UnimCodigo": "1",
        })

    arr_datos = {
        "Solicitud": {
            "Nonce": "af4c65a3-0a18-4b09-8ca7-475c95b45894",
            "Suscriptor": arr_factura['dat_suscriptor'],
        },
        "FacturaVenta": {
            "Cabecera": {
                "DoceManejaPeriodos": 0,
                "DoceConsecutivo": numero,
                "DoceCantidadItems": arr_factura['doc_cantidad_item'],
                "AmbdCodigo": arr_factura['dat_tipoAmbiente'],
                "TipoCodigo": tipo_codigo,
                "DoetCodigo": tipo,
                "MoneCodigo": "COP",
                "RefvNumero": arr_factura['res_numero'],
                "EnviarSetPruebas": 0
            },
            "PagosFactura": {
                "ForpCodigo": forma_pago,
                "DoepFechaVencimiento": fecha_vencimiento + 'T' + hora,
                "Medios": [
                    {
                        "DempCodigo": "31",
                        "DempDescripcion": " ",
                    }
                ]
            },
            "Observaciones": [],
            "Referencias": [],
            "ordenDocumento": {
                "DeorNumeroOrden": arr_factura['doc_orden_compra'] if arr_factura['doc_orden_compra'] else '',
                "DeorTipoOrden": '',
                "DeorFechaOrden": '',
                "DeorDocumentoReferencia": '',
            },
            "AdquirienteFactura": {
                "DoeaEsResponsable": 1,
                "DoeaEsnacional": 1,
                "TidtCodigo": arr_factura['ad_tipoIdentificacion'],
                "DoeaDocumento": arr_factura['ad_numeroIdentificacion'],
                "DoeaDiv": arr_factura['ad_digitoVerificacion'],
                "DoeaRazonSocial": arr_factura['ad_nombreCompleto'],
                "DoeaNombreCiudad": arr_factura['ad_nombreCiudad'],
                "DoeaNombreDepartamento": arr_factura['ad_nombreDepartamento'],
                "DoeaPais": "CO",
                "DoeaDireccion": arr_factura['ad_direccion'],
                "DoeaObligaciones": "O-99",
                "DoeaNombres": "",
                "DoeaApellidos": "",
                "DoeaOtrosNombres": "",
                "DoeaCorreo": arr_factura['ad_correo'],
                "DoeaTelefono": arr_factura['ad_telefono'],
                "TiotCodigo": arr_factura['ad_tipoPersona'],
                "RegCodigo": "49",
                "CopcCodigo": arr_factura['ad_codigoPostal'],
                "DoeaManejoAdjuntos": 1,
            },
            "ImpuestosFactura": [
                {
                    "DoeiTotal": arr_factura['doc_iva'],
                    "DoeiEsPorcentual": 1,
                    "ImpuCodigo": "01",
                    "Detalle": arr_impuestos,
                }
            ],
            "PeriodoFactura": {
                "DoepFechaInicial": str(arr_factura['doc_fecha']) + 'T' + str(arr_factura['doc_hora2']),
                "DoepFechaFinal": str(arr_factura['doc_fecha_vence']) + 'T' + str(arr_factura['doc_hora2']),
            },
            "ResumenImpuestosFactura": {
                "DeriTotalIva": arr_factura['doc_iva'],
                "DeriTotalConsumo": 0,
                "DeriTotalIca": 0,
            },
            "TotalesFactura": {
                "DoetSubtotal": arr_factura['doc_subtotal'],
                "DoetBase": arr_factura['doc_baseIva'],
                "DoetTotalImpuestos": arr_factura['doc_iva'],
                "DoetSubtotalMasImpuestos": arr_factura['doc_total'],
                "DoetTotalDescuentos": 0,
                "DoetTotalcargos": 0,
                "DoetTotalAnticipos": 0,
                "DoetTotalDocumento": arr_factura['doc_total'],
            },
        },
    }

    arr_datos['FacturaVenta']['DetalleFactura'] = []

    for item in arr_factura['doc_itemes']:
        arr_datos['FacturaVenta']['DetalleFactura'].append({
            "DoeiItem": item['item_id'],
            "DoeiCodigo": item['item_codigo'],
            "DoeiDescripcion": item['item_nombre'],
            "DoeiMarca": "",
            "DoeiModelo": "",
            "DoeiObservacion": "",
            "DoeiDatosVendedor": "",
            "DoeiCantidad": item['item_cantidad'],
            "DoeiCantidadEmpaque": item['item_cantidad'],
            "DoeiEsObsequio": 0,
            "DoeiPrecioUnitario": item['item_precio'],
            "DoeiPrecioReferencia": item['item_precio'],
            "DoeiValor": item['item_precio'],
            "DoeiTotalDescuentos": 0,
            "DoeiTotalCargos": 0,
            "DoeiTotalImpuestos": item['item_iva'],
            "DoeiBase": item['item_base_iva'],
            "DoeiSubtotal": item['item_subtotal'],
            "TicpCodigo": "999",
            "UnimCodigo": "94",
            "CtprCodigo": "02",
            "ImpuestosLinea": [
                {
                    "DoeiTotal": item['item_iva'],
                    "DoeiEsPorcentual": 1,
                    "ImpuCodigo": "01",
                    "Detalle": [
                        {
                            "DediBase": item['item_base_iva'],
                            "DediValor": item['item_iva'],
                            "DediFactor": item['item_porcentaje_iva'],
                            "UnimCodigo": "1",
                        }
                    ]
                }
            ],
            "ImpuestosRetenidosLinea": [],
            "CargosDescuentosLinea": [],
        })

    if tipo == '91' or tipo == '92':
        codigo_concepto = 2 if arr_factura['ref_codigoExterno'] else 4
        if arr_factura['doc_concepto']:
            codigo_concepto = arr_factura['doc_concepto']

        arr_datos['FacturaVenta']['DocumentoReferencia'] = {
            "DedrDocumentoReferencia": arr_factura['ref_codigoExterno'] if arr_factura['ref_codigoExterno'] else None,
            "CodigoConcepto": codigo_concepto,
        }

    return arr_datos
