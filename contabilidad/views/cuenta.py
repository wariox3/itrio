from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.cuenta_clase import ConCuentaClase
from contabilidad.models.cuenta_grupo import ConCuentaGrupo
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta
from contabilidad.models.cuenta_subcuenta import ConCuentaSubcuenta
from contabilidad.serializers.cuenta import ConCuentaSerializador
from io import BytesIO
import base64
import openpyxl
import gc

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuenta.objects.all()
    serializer_class = ConCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raw = request.data        
        codigo = raw.get('codigo')
        validar_cuenta = ConCuenta.objects.filter(codigo=codigo).exists()    
        if validar_cuenta:
            return Response({'mensaje':'Ya existe una cuenta con este codigo', 'codigo':14}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

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
                    'exige_tercero': row[2],
                    'exige_base': row[3],
                    'exige_grupo': row[4],
                    'permite_movimiento': row[5],
                    'cuenta_clase_id': None,
                    'cuenta_grupo_id': None,
                    'cuenta_cuenta_id': None,
                    'nivel': None                    
                }  
                if not data['codigo']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un codigo'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    cuenta = ConCuenta.objects.filter(codigo=data['codigo']).first()
                    if cuenta:
                        error_dato = {
                            'fila': i,
                            'Mensaje': f'La cuenta {data["codigo"]} ya existe'
                        }
                        errores_datos.append(error_dato)
                        errores = True
                    else:
                        codigo_str = str(data['codigo'])
                        longitud_codigo = len(codigo_str)
                        if longitud_codigo == 1:                            
                            cuenta_clase_id = codigo_str[0]
                            if not ConCuentaClase.objects.filter(id=cuenta_clase_id).exists():
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'La clase {cuenta_clase_id} no existe'
                                }
                                errores_datos.append(error_dato)
                                errores = True

                        if longitud_codigo == 2:
                            cuenta_grupo_id = codigo_str[:2]                        
                            if not ConCuentaGrupo.objects.filter(id=cuenta_grupo_id).exists():
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'El grupo {cuenta_grupo_id} no existe'
                                }
                                errores_datos.append(error_dato)
                                errores = True    

                        if longitud_codigo == 4:
                            cuenta_cuenta_id = codigo_str[:4]                            
                            if not ConCuentaCuenta.objects.filter(id=cuenta_cuenta_id).exists():
                                error_dato = {
                                    'fila': i,
                                    'Mensaje': f'La cuenta {cuenta_cuenta_id} no existe'
                                }
                                errores_datos.append(error_dato)
                                errores = True 
                        if longitud_codigo >= 1:
                            data['cuenta_clase_id'] = codigo_str[0]
                        if longitud_codigo >= 2:
                            data['cuenta_grupo_id'] = codigo_str[:2]
                        if longitud_codigo >= 4:                            
                            data['cuenta_cuenta_id'] = codigo_str[:4]
                        if longitud_codigo <= 1:
                            data['nivel'] = 1
                        if longitud_codigo > 1 and longitud_codigo <= 2:
                            data['nivel'] = 2
                        if longitud_codigo > 2 and longitud_codigo <= 4:
                            data['nivel'] = 3  
                        if longitud_codigo > 4 and longitud_codigo <= 6:
                            data['nivel'] = 4
                        if longitud_codigo > 6 and longitud_codigo <= 8:
                            data['nivel'] = 5
                        if longitud_codigo > 8:
                            error_dato = {
                                'fila': i,
                                'Mensaje': f'La cuenta tiene una longitud invalida'
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
                        cuenta_clase_id=detalle['cuenta_clase_id'],
                        cuenta_grupo_id=detalle['cuenta_grupo_id'],
                        cuenta_cuenta_id=detalle['cuenta_cuenta_id'],
                        exige_tercero=detalle['exige_tercero'],
                        exige_base=detalle['exige_base'],
                        exige_grupo=detalle['exige_grupo'],
                        permite_movimiento=detalle['permite_movimiento'],
                        nivel=detalle['nivel']
                    )
                    registros_importados += 1
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:            
                gc.collect()                    
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    