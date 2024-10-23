from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.adicional import HumAdicional
from humano.models.programacion import HumProgramacion
from humano.serializers.adicional import HumAdicionalSerializador
from io import BytesIO
import base64
import openpyxl

class HumAdicionalViewSet(viewsets.ModelViewSet):
    queryset = HumAdicional.objects.all()
    serializer_class = HumAdicionalSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'importar',)
    def importar(self, request):
        raw = request.data        
        archivo_base64 = raw.get('archivo_base64')
        permanente = raw.get('permanente')
        if archivo_base64:
            if permanente == True:
                programacion_id = None
            else:
                programacion_id = raw.get('programacion_id', None)
                if programacion_id:
                    programacion = HumProgramacion.objects.filter(id=programacion_id).first()
                    if not programacion:
                        return Response({'mensaje':'La programacion no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 
                else:
                   return Response({'mensaje':'Si el adicional no es permanente debe tener el id de la programacion', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

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
                    'identificacion': row[0],
                    'contrato_id':row[1],
                    'concepto_id':row[2],
                    'valor':row[3],
                    'detalle':row[4],
                    'aplica_dia_laborado':row[5],
                }  
                if not data['identificacion']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar un numero identificacion'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['contrato_id']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el id del contrato'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['concepto_id']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el id del concepto'
                    }
                    errores_datos.append(error_dato)
                    errores = True

                if not data['valor']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar el valor'
                    }
                    errores_datos.append(error_dato)
                    errores = True    

                if not data['aplica_dia_laborado']:
                    error_dato = {
                        'fila': i,
                        'Mensaje': 'Debe digitar si aplica dia laborado'
                    }
                    errores_datos.append(error_dato)
                    errores = True
                else:
                    if data['aplica_dia_laborado'] in ['SI', 'NO']:
                        data['aplica_dia_laborado'] = data['aplica_dia_laborado'] == 'SI'
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
                    HumAdicional.objects.create(
                        contrato_id=detalle['contrato_id'],
                        concepto_id=detalle['concepto_id'],
                        valor=detalle['valor'],
                        detalle=detalle['detalle'],
                        aplica_dia_laborado=detalle['aplica_dia_laborado'],
                        permanente = permanente,
                        programacion_id = programacion_id
                    )
                    registros_importados += 1
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                return Response({'errores': True, 'errores_datos': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     