from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.models.comprobante import ConComprobante
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.grupo import ConGrupo
from contabilidad.models.periodo import ConPeriodo
from general.models.contacto import GenContacto
from contabilidad.serializers.movimiento import ConMovimientoSerializador
from datetime import datetime
from io import BytesIO
from django.db.models import F,Sum
import base64
import openpyxl
import json
import gc

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
                    'fecha': None,
                    'debito': row[2] if row[2] is not None else 0,
                    'credito': row[3] if row[3] is not None else 0,
                    'base': row[4] if row[4] is not None else 0, 
                    'naturaleza': None,
                    'comprobante': row[5],
                    'cuenta': row[6],
                    'grupo': row[7],
                    'contacto': row[8],
                    'detalle': row[9],
                    'periodo': None,
                    'documento': None
                }  

                if row[1]:
                    fecha = row[1]        
                    data['periodo'] = fecha[:6]
                    fecha_valida = datetime.strptime(fecha, "%Y%m%d").date()
                    data['fecha'] = fecha_valida                 

                if data['cuenta']:
                    cuenta = ConCuenta.objects.filter(codigo=data['cuenta']).first()
                    if cuenta:
                        data['cuenta'] = cuenta.id 

                if data['grupo']:
                    grupo = ConGrupo.objects.filter(codigo=data['grupo']).first()
                    if grupo:
                        data['grupo'] = grupo.id                         

                if data['contacto']:
                    contacto = GenContacto.objects.filter(numero_identificacion=data['contacto']).first()
                    if contacto:
                        data['contacto'] = contacto.id                        
                
                naturaleza = 'D'
                if data['credito'] > 0:
                    naturaleza = 'C'
                data['naturaleza'] = naturaleza

                serializer = ConMovimientoSerializador(data=data)
                if serializer.is_valid():
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
                    ConMovimiento.objects.create(**detalle)
                gc.collect()
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:
                gc.collect()                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)                                          
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    @action(detail=False, methods=["post"], url_path=r'informe-balance-prueba',)
    def informe_balance_prueba(self, request):    
        
        query = '''
            SELECT
                c.id,
                c.codigo,
                c.cuenta_clase_id ,
                c.cuenta_grupo_id ,
                c.cuenta_cuenta_id ,
                c.nivel,                      
                (SELECT SUM(debito) FROM con_movimiento m WHERE m.cuenta_id = c.id AND m.periodo_id < 202408) AS vr_debito_anterior,
                (SELECT SUM(credito) FROM con_movimiento m WHERE m.cuenta_id = c.id AND m.periodo_id < 202408) AS vr_credito_anterior,      
                (SELECT SUM(debito) FROM con_movimiento m WHERE m.cuenta_id = c.id AND (m.periodo_id >= 202409 AND m.periodo_id <= 202409)) AS vr_debito,
                (SELECT SUM(credito) FROM con_movimiento m WHERE m.cuenta_id = c.id AND (m.periodo_id >= 202409 AND m.periodo_id <= 202409)) AS vr_credito      
            FROM
                con_cuenta c
        '''
        resultados = ConCuenta.objects.raw(query)
        resultados_json = [
            {
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'cuenta_clase_id': cuenta.cuenta_clase_id,
                'cuenta_grupo_id': cuenta.cuenta_grupo_id,
                'cuenta_cuenta_id': cuenta.cuenta_cuenta_id,
                'nivel': cuenta.nivel,
                'vr_debito_anterior': cuenta.vr_debito_anterior,
                'vr_credito_anterior': cuenta.vr_credito_anterior,
                'vr_debito': cuenta.vr_debito,
                'vr_credito': cuenta.vr_credito,
            }
            for cuenta in resultados
        ]
        return Response({'movimientos': resultados_json}, status=status.HTTP_200_OK)