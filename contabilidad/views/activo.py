from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.activo import ConActivo
from contabilidad.models.cuenta import ConCuenta
from contabilidad.serializers.activo import ConActivoSerializador
from django.db.models import ProtectedError
from datetime import datetime
from io import BytesIO
import base64
import openpyxl
import gc
import os

class ActivoViewSet(viewsets.ModelViewSet):
    queryset = ConActivo.objects.all()
    serializer_class = ConActivoSerializador
    permission_classes = [permissions.IsAuthenticated]

    def calcular_depreciacion_periodo(self, valor_compra, duracion):
        valor_compra = float(valor_compra)
        duracion = int(duracion)
        if duracion > 0:
            return valor_compra / duracion
        return 0

    def perform_create(self, serializer):
        raw = self.request.data
        valor_compra = raw.get('valor_compra')
        duracion = raw.get('duracion')
        depreciacion_periodo = self.calcular_depreciacion_periodo(valor_compra, duracion)
        serializer.save(depreciacion_periodo=depreciacion_periodo, depreciacion_saldo=valor_compra)

    def perform_update(self, serializer):
        raw = self.request.data
        valor_compra = raw.get('valor_compra')
        duracion = raw.get('duracion')
        depreciacion_periodo = self.calcular_depreciacion_periodo(valor_compra, duracion)
        serializer.save(depreciacion_periodo=depreciacion_periodo, depreciacion_saldo=valor_compra)          
        
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
                    'marca': row[2],
                    'serie': row[3],
                    'modelo': row[4],
                    'fecha_compra': row[5],
                    'fecha_activacion': row[6],
                    'fecha_baja': row[7],
                    'duracion': row[8],
                    'valor_compra': row[9],
                    'depreciacion_inicial': row[10],
                    'activo_grupo': row[11],
                    'cuenta_depreciacion': int(row[12]),
                    'cuenta_gasto': int(row[13]),
                    'grupo': row[14],
                    'metodo_depreciacion': row[15],
                }  

                if not data['codigo']:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'fecha_compra': ['Debe digitar un código']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue

                if not data['nombre']:
                    errores = True  
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'fecha_compra': ['Debe digitar un nombre']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue  

                if not data['fecha_compra']:
                    errores = True    
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'fecha_compra': ['Debe ingresar la fecha de compra']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue  

                if not data['fecha_activacion']:
                    errores = True   
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'fecha_activacion': ['Debe ingresar la fecha de activación']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue  

                if row[5]:
                    fechaDesde = str(row[5])   
                    fecha_valida = datetime.strptime(fechaDesde, "%Y%m%d").date()
                    data['fecha_compra'] = fecha_valida

                if row[6]:
                    fechaHasta = str(row[6])
                    fecha_valida = datetime.strptime(fechaHasta, "%Y%m%d").date()
                    data['fecha_activacion'] = fecha_valida

                if not data['duracion']:
                    errores = True    
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'duracion': ['Debe digitar la duración.']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue  

                if not data['valor_compra']:
                    errores = True    
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'valor_compra': ['Debe digitar el valor de la compra.']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue  

                if not data['depreciacion_inicial']:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': {
                            'depreciacion_inicial': ['Debe digitar el valor de la depreciación inicial.']
                        }
                    }
                    errores_datos.append(error_dato)  
                    continue  

                if data['cuenta_depreciacion']:
                    cuentaDepreciacion = ConCuenta.objects.filter(codigo=data['cuenta_depreciacion']).first()
                    if cuentaDepreciacion:
                        data['cuenta_depreciacion'] = cuentaDepreciacion.id


                if data['cuenta_gasto']:
                    cuentaGasto = ConCuenta.objects.filter(codigo=data['cuenta_gasto']).first()
                    if cuentaGasto:
                        data['cuenta_depreciacion'] = cuentaGasto.id

                # Calcular la depreciación por período
                valor_compra = float(data['valor_compra'])
                duracion = int(data['duracion'])
                if duracion > 0:
                    depreciacion_periodo = valor_compra / duracion
                    # Redondear a 6 decimales
                    depreciacion_periodo = round(depreciacion_periodo, 6)
                    data['depreciacion_periodo'] = depreciacion_periodo
                    data['depreciacion_saldo'] = valor_compra


                serializer = ConActivoSerializador(data=data)
                if serializer.is_valid():
                    validated_data = serializer.validated_data
                    validated_data['depreciacion_periodo'] = depreciacion_periodo
                    validated_data['depreciacion_saldo'] = valor_compra
                    data_modelo.append(serializer.validated_data)
                    registros_importados += 1
                else:
                    errores = True
                    error_dato = {
                        'fila': i,
                        'errores': serializer.errors
                    }                                    
                    errores_datos.append(error_dato)    

            if not errores:
                for detalle in data_modelo:
                    ConActivo.objects.create(**detalle)
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        