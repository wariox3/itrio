from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.cuenta import ConCuenta
from contabilidad.serializers.cuenta import ConCuentaSerializador
from io import BytesIO
import base64
import openpyxl
import gc

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuenta.objects.all()
    serializer_class = ConCuentaSerializador
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
                    'codigo': row[0],
                    'nombre':row[1],
                    'clase_id': row[2],
                    'exige_tercero': row[3],
                    'exige_base': row[4],
                    'exige_grupo': row[5],
                    'permite_movimiento': row[6]
                }  
                if not data['codigo']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un codigo'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['nombre']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar nombre'
                    }
                    errores_datos.append(error_dato)
                    errores = True                                 

                if not data['clase_id']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un codigo'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['exige_tercero']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si la cuenta exige tercero'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['exige_tercero'] in ['SI', 'NO']:
                        data['exige_tercero'] = data['exige_tercero'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True                                        

                if not data['exige_base']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si la cuenta exige base'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['exige_base'] in ['SI', 'NO']:
                        data['exige_base'] = data['exige_base'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True                    

                if not data['exige_grupo']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si la cuenta exige grupo'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['exige_grupo'] in ['SI', 'NO']:
                        data['exige_grupo'] = data['exige_grupo'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True

                if not data['permite_movimiento']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si la cuenta permite movimiento'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['permite_movimiento'] in ['SI', 'NO']:
                        data['permite_movimiento'] = data['permite_movimiento'] == 'SI'
                    else:
                        error_dato = {
                            'fila': i,
                            'Mensaje': 'Los valores validos son SI o NO'
                        }
                        errores_datos.append(error_dato)
                        errores = True                        
                data_modelo.append(data)
            if errores == False:
                for detalle in data_modelo:
                    ConCuenta.objects.create(
                        codigo=detalle['codigo'],
                        nombre=detalle['nombre'],
                        cuenta_clase_id=detalle['clase_id'],
                        exige_tercero=detalle['exige_tercero'],
                        exige_base=detalle['exige_base'],
                        exige_grupo=detalle['exige_grupo'],
                        permite_movimiento=detalle['permite_movimiento']
                    )
                    registros_importados += 1                                
                #gc.collect()
                wb.close()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:                                
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    