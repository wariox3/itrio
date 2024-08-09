from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.models.comprobante import ConComprobante
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.grupo import ConGrupo
from general.models.contacto import GenContacto
from contabilidad.serializers.movimiento import ConMovimientoSerializador
from datetime import datetime
from io import BytesIO
import base64
import openpyxl

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = ConMovimiento.objects.all()
    serializer_class = ConMovimientoSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        if archivo_base64:
            try:
                archivo_data = base64.b64decode(archivo_base64)
                archivo = BytesIO(archivo_data)
                wb = openpyxl.load_workbook(archivo)
                sheet = wb.active    
            except Exception as e:     
                return Response({f'mensaje':'Error procesando el archivo, valide que es un archivo de excel .xlsx', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)  
            
            data_modelo = []
            errores = False
            errores_datos = []
            registros_importados = 0
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                data = {
                    'numero': row[0],
                    'fecha':row[1],
                    'debito': row[2] if row[2] is not None else 0,
                    'credito': row[3] if row[3] is not None else 0,
                    'base': row[4] if row[4] is not None else 0, 
                    'naturaleza': row[5],
                    'comprobante': row[6],
                    'cuenta': row[7],
                    'grupo': row[8],
                    'numero_identificacion': row[9],
                    'detalle': row[10],
                }  

                if not data['fecha']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar fecha'
                    }
                    errores_datos.append(error_dato)
                    errores = True   

                if not data['naturaleza']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar la naturaleza'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['naturaleza'] not in ['D', 'C']:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son D o C'
                        }
                        errores_datos.append(error_dato)
                        errores = True                    

                if not data['comprobante']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el codigo de comprobante'
                    }
                    errores_datos.append(error_dato)
                    errores = True  
                else:
                    comprobante = ConComprobante.objects.filter(codigo=data['comprobante']).first()
                    if comprobante is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El comprobante con codigo {data["comprobante"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['comprobante_id'] = comprobante.id 

                if not data['cuenta']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el codigo de cuenta'
                    }
                    errores_datos.append(error_dato)
                    errores = True  
                else:
                    cuenta = ConCuenta.objects.filter(codigo=data['cuenta']).first()
                    if cuenta is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'La cuenta con codigo {data["cuenta"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['cuenta_id'] = cuenta.id 

                if data['grupo']:
                    grupo = ConGrupo.objects.filter(codigo=data['grupo']).first()
                    if grupo is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El grupo con codigo {data["grupo"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['grupo_id'] = grupo.id 
                else:
                    data['grupo_id'] = None

                if data['numero_identificacion']:
                    contacto = GenContacto.objects.filter(numero_identificacion=data['numero_identificacion']).first()
                    if contacto is None:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El contacto con numero identificacion {data["numero_identificacion"]} no existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        data['contacto_id'] = contacto.id

                if data['detalle']:
                    if len(data['detalle']) > 150:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'El maximo numero de caracteres del detalle puede ser de 150'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                data_modelo.append(data)
            if errores == False:
                for detalle in data_modelo:
                    fecha_formateada = datetime.strptime(detalle['fecha'], "%Y%m%d").strftime("%Y-%m-%d")
                    ConMovimiento.objects.create(
                        numero=detalle['numero'],
                        fecha=fecha_formateada,
                        debito=detalle['debito'],
                        credito=detalle['credito'],
                        base=detalle['base'],
                        naturaleza=detalle['naturaleza'],
                        detalle=detalle['detalle'],
                        comprobante_id=detalle['comprobante_id'],
                        cuenta_id=detalle['cuenta_id'],
                        grupo_id=detalle['grupo_id'],
                        contacto_id=detalle['contacto_id']
                    )
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    