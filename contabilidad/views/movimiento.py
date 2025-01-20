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
        

            #opcion con filtros
    @action(detail=False, methods=["post"], url_path=r'informe-balance-prueba',)
    def informe_balance_prueba(self, request):    
        filtros = request.data.get("filtros", [])

        # Extraer las fechas desde los filtros
        fecha_desde = None
        fecha_hasta = None
        for filtro in filtros:
            if filtro["propiedad"] == "fecha_desde__gte":
                fecha_desde = filtro["valor1"]
            if filtro["propiedad"] == "fecha_hasta__lte":
                fecha_hasta = filtro["valor1"]
        
        # Validar que las fechas estén presentes
        if not fecha_desde or not fecha_hasta:
            return Response(
                {"error": "Los filtros 'fecha_desde' y 'fecha_hasta' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        query = f'''
            SELECT
                c.id,
                c.codigo,
                c.nombre,
                c.cuenta_clase_id,
                c.cuenta_grupo_id,
                c.cuenta_cuenta_id,
                c.nivel,
                COALESCE(SUM(CASE WHEN m.fecha < '{fecha_desde}' THEN m.debito ELSE 0 END), 0) AS debito_anterior,
                COALESCE(SUM(CASE WHEN m.fecha < '{fecha_desde}' THEN m.credito ELSE 0 END), 0) AS credito_anterior,
                COALESCE(SUM(CASE WHEN m.fecha BETWEEN '{fecha_desde}' AND '{fecha_hasta}' THEN m.debito ELSE 0 END), 0) AS debito,
                COALESCE(SUM(CASE WHEN m.fecha BETWEEN '{fecha_desde}' AND '{fecha_hasta}' THEN m.credito ELSE 0 END), 0) AS credito
            FROM
                con_cuenta c
            LEFT JOIN
                con_movimiento m ON m.cuenta_id = c.id
            GROUP BY
                c.id, c.codigo, c.nombre, c.cuenta_clase_id, c.cuenta_grupo_id, c.cuenta_cuenta_id, c.nivel
            ORDER BY
                c.cuenta_clase_id,
                c.cuenta_grupo_id,
                c.cuenta_cuenta_id;
        '''
        # Ejecutar la consulta
        resultados = ConCuenta.objects.raw(query)
        
        # Procesar los resultados como en tu lógica original
        resultados_json = []
        clases_dict = {}
        grupos_dict = {}
        cuentas_dict = {}
        for cuenta in resultados:
            saldo_anterior = cuenta.debito_anterior - cuenta.credito_anterior
            saldo_actual = saldo_anterior + (cuenta.debito - cuenta.credito)
            resultados_json.append({
                'tipo': 'movimiento',
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'cuenta_clase_id': cuenta.cuenta_clase_id,
                'cuenta_grupo_id': cuenta.cuenta_grupo_id,
                'cuenta_cuenta_id': cuenta.cuenta_cuenta_id,
                'nivel': cuenta.nivel,
                'saldo_anterior': saldo_anterior,
                'debito': cuenta.debito,
                'credito': cuenta.credito,
                'saldo_actual': saldo_actual
            })
            
            # Agrupación en clases, grupos y cuentas
            clase_id = cuenta.cuenta_clase_id
            if clase_id not in clases_dict:
                clases_dict[clase_id] = {
                    'tipo': 'clase',
                    'id': clase_id,
                    'codigo': str(clase_id),
                    'nombre': "",
                    'cuenta_clase_id': clase_id,
                    'nivel': 1,
                    'saldo_anterior': 0,
                    'debito': 0,
                    'credito': 0,
                    'saldo_actual': 0
                }
            clases_dict[clase_id]['saldo_anterior'] += saldo_anterior
            clases_dict[clase_id]['debito'] += cuenta.debito
            clases_dict[clase_id]['credito'] += cuenta.credito
            clases_dict[clase_id]['saldo_actual'] += saldo_actual
            
            grupo_id = cuenta.cuenta_grupo_id
            if grupo_id not in grupos_dict:
                grupos_dict[grupo_id] = {
                    'tipo': 'grupo',
                    'id': grupo_id,
                    'codigo': str(grupo_id),
                    'nombre': "",
                    'cuenta_grupo_id': grupo_id,
                    'saldo_anterior': 0,
                    'debito': 0,
                    'credito': 0,
                    'saldo_actual': 0
                }
            grupos_dict[grupo_id]['saldo_anterior'] += saldo_anterior
            grupos_dict[grupo_id]['debito'] += cuenta.debito
            grupos_dict[grupo_id]['credito'] += cuenta.credito
            grupos_dict[grupo_id]['saldo_actual'] += saldo_actual

            cuenta_id = cuenta.cuenta_cuenta_id
            if cuenta_id not in cuentas_dict:
                cuentas_dict[cuenta_id] = {
                    'tipo': 'cuenta',
                    'id': cuenta_id,
                    'codigo': str(cuenta_id),
                    'nombre': "",
                    'cuenta_cuenta_id': cuenta_id,
                    'saldo_anterior': 0,
                    'debito': 0,
                    'credito': 0,
                    'saldo_actual': 0
                }
            cuentas_dict[cuenta_id]['saldo_anterior'] += saldo_anterior
            cuentas_dict[cuenta_id]['debito'] += cuenta.debito
            cuentas_dict[cuenta_id]['credito'] += cuenta.credito
            cuentas_dict[cuenta_id]['saldo_actual'] += saldo_actual
        
        # Agregar las clases, grupos y cuentas al resultado final
        resultados_json.extend(clases_dict.values())
        resultados_json.extend(grupos_dict.values())
        resultados_json.extend(cuentas_dict.values())
        resultados_json.sort(key=lambda x: str(x['codigo']))
        
        return Response({'registros': resultados_json}, status=status.HTTP_200_OK)
        
    # @action(detail=False, methods=["post"], url_path=r'informe-balance-prueba',)
    # def informe_balance_prueba(self, request):    
        
    #     query = '''
    #                 SELECT
    #                     c.id,
    #                     c.codigo,
    #                     c.nombre,
    #                     c.cuenta_clase_id,                        
    #                     c.cuenta_grupo_id,
    #                     c.cuenta_cuenta_id,
    #                     c.nivel,
    #                     COALESCE(SUM(CASE WHEN m.periodo_id < 202410 THEN m.debito ELSE 0 END), 0) AS debito_anterior,
    #                     COALESCE(SUM(CASE WHEN m.periodo_id < 202410 THEN m.credito ELSE 0 END), 0) AS credito_anterior,
    #                     COALESCE(SUM(CASE WHEN m.periodo_id BETWEEN 202410 AND 202410 THEN m.debito ELSE 0 END), 0) AS debito,
    #                     COALESCE(SUM(CASE WHEN m.periodo_id BETWEEN 202410 AND 202410 THEN m.credito ELSE 0 END), 0) AS credito
    #                 FROM
    #                     con_cuenta c
    #                 LEFT JOIN
    #                     con_movimiento m ON m.cuenta_id = c.id
    #                 GROUP BY
    #                     c.id, c.codigo, c.nombre, c.cuenta_clase_id, c.cuenta_grupo_id, c.cuenta_cuenta_id, c.nivel
    #                 ORDER BY
    #                     c.cuenta_clase_id,
    #                     c.cuenta_grupo_id,
    #                     c.cuenta_cuenta_id;
    #     '''
    #     resultados = ConCuenta.objects.raw(query)
    #     resultados_json = []
    #     clases_dict = {}
    #     grupos_dict = {}
    #     cuentas_dict = {}
    #     for cuenta in resultados:
    #         saldo_anterior = cuenta.debito_anterior - cuenta.credito_anterior
    #         saldo_actual = saldo_anterior + (cuenta.debito - cuenta.credito)
    #         resultados_json.append({
    #             'tipo': 'movimiento',
    #             'id': cuenta.id,
    #             'codigo': cuenta.codigo,
    #             'nombre': cuenta.nombre,
    #             'cuenta_clase_id': cuenta.cuenta_clase_id,
    #             'cuenta_grupo_id': cuenta.cuenta_grupo_id,
    #             'cuenta_cuenta_id': cuenta.cuenta_cuenta_id,
    #             'nivel': cuenta.nivel,
    #             'saldo_anterior': saldo_anterior,                
    #             'debito': cuenta.debito,
    #             'credito': cuenta.credito,
    #             'saldo_actual': saldo_actual
    #         })  
    #         clase_id = cuenta.cuenta_clase_id
    #         if clase_id not in clases_dict:  
    #             clases_dict[clase_id] = {
    #                 'tipo': 'clase',
    #                 'id': clase_id,
    #                 'codigo': str(clase_id),
    #                 'nombre': "",
    #                 'cuenta_clase_id': clase_id,
    #                 'nivel': 1,
    #                 'saldo_anterior': 0,
    #                 'debito': 0,
    #                 'credito': 0,
    #                 'saldo_actual': 0
    #             }
    #         clases_dict[clase_id]['saldo_anterior'] += saldo_anterior
    #         clases_dict[clase_id]['debito'] += cuenta.debito
    #         clases_dict[clase_id]['credito'] += cuenta.credito
    #         clases_dict[clase_id]['saldo_actual'] += saldo_actual
        
    #         grupo_id = cuenta.cuenta_grupo_id
    #         if grupo_id not in grupos_dict:  
    #             grupos_dict[grupo_id] = {
    #                 'tipo': 'grupo',
    #                 'id': grupo_id,
    #                 'codigo': str(grupo_id),
    #                 'nombre': "",
    #                 'cuenta_grupo_id': grupo_id,
    #                 'saldo_anterior': 0,
    #                 'debito': 0,
    #                 'credito': 0,
    #                 'saldo_actual': 0
    #             }
    #         grupos_dict[grupo_id]['saldo_anterior'] += saldo_anterior
    #         grupos_dict[grupo_id]['debito'] += cuenta.debito
    #         grupos_dict[grupo_id]['credito'] += cuenta.credito
    #         grupos_dict[grupo_id]['saldo_actual'] += saldo_actual

    #         cuenta_id = cuenta.cuenta_cuenta_id
    #         if cuenta_id not in cuentas_dict:  
    #             cuentas_dict[cuenta_id] = {
    #                 'tipo': 'cuenta',
    #                 'id': cuenta_id,
    #                 'codigo': str(cuenta_id),
    #                 'nombre': "",
    #                 'cuenta_cuenta_id': cuenta_id,
    #                 'saldo_anterior': 0,
    #                 'debito': 0,
    #                 'credito': 0,
    #                 'saldo_actual': 0
    #             }
    #         cuentas_dict[cuenta_id]['saldo_anterior'] += saldo_anterior
    #         cuentas_dict[cuenta_id]['debito'] += cuenta.debito
    #         cuentas_dict[cuenta_id]['credito'] += cuenta.credito
    #         cuentas_dict[cuenta_id]['saldo_actual'] += saldo_actual
            
    #     resultados_json.extend(clases_dict.values())
    #     resultados_json.extend(grupos_dict.values())
    #     resultados_json.extend(cuentas_dict.values())
    #     resultados_json.sort(key=lambda x: str(x['codigo']))

    #     return Response({'registros': resultados_json}, status=status.HTTP_200_OK)