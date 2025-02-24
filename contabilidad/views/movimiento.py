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
from io import BytesIO
from django.http import HttpResponse
from utilidades.excel import WorkbookEstilos
from openpyxl import Workbook
from general.formatos.balance_prueba import FormatoBalancePrueba
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
            cuentas_map = {c.codigo: c.id for c in ConCuenta.objects.all()}
            grupos_map = {g.codigo: g.id for g in ConGrupo.objects.all()}
            contactos_map = {ct.numero_identificacion: ct.id for ct in GenContacto.objects.all()}
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
                    'periodo': row[10],
                    'cierre': row[11],
                    'documento': None
                }  

                if row[1]:       
                    fecha_valida = datetime.strptime(row[1], "%Y%m%d").date()
                    data['fecha'] = fecha_valida                 
                
                data['cuenta'] = cuentas_map.get(data['cuenta'])
                data['grupo'] = grupos_map.get(data['grupo'])
                data['contacto'] = contactos_map.get(data['contacto'])

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
                ConMovimiento.objects.bulk_create([ConMovimiento(**detalle) for detalle in data_modelo])
                return Response({'registros_importados': registros_importados}, status=status.HTTP_200_OK)
            else:                    
                return Response({'mensaje':'Errores de validacion', 'codigo':1, 'errores_validador': errores_datos}, status=status.HTTP_400_BAD_REQUEST)        
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    def obtener_balance_prueba(self, fecha_desde, fecha_hasta, cierre = False):
        parametro_cierre = ' AND m.cierre = false '
        if cierre == True:
            parametro_cierre = ''
            
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
                COALESCE(SUM(CASE WHEN m.fecha BETWEEN '{fecha_desde}' AND '{fecha_hasta}' {parametro_cierre} THEN m.debito ELSE 0 END), 0) AS debito,
                COALESCE(SUM(CASE WHEN m.fecha BETWEEN '{fecha_desde}' AND '{fecha_hasta}' {parametro_cierre} THEN m.credito ELSE 0 END), 0) AS credito
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
        resultados = ConCuenta.objects.raw(query)
        
        # Procesar resultados
        resultados_json = []
        clases_dict = {}
        grupos_dict = {}
        cuentas_dict = {}
        for cuenta in resultados:
            saldo_anterior = cuenta.debito_anterior - cuenta.credito_anterior
            saldo_actual = saldo_anterior + (cuenta.debito - cuenta.credito)
            resultados_json.append({
                'tipo': 'AUXILIAR',
                'id': cuenta.id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'contacto_id': None,
                'contacto_nombre': None,
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
                    'tipo': 'CLASE',
                    'id': clase_id,
                    'codigo': str(clase_id),
                    'nombre': "",
                    'contacto_id': None,
                    'contacto_nombre': None,                    
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
                    'tipo': 'GRUPO',
                    'id': grupo_id,
                    'codigo': str(grupo_id),
                    'nombre': "",
                    'contacto_id': None,
                    'contacto_nombre': None,                    
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
                    'tipo': 'CUENTA',
                    'id': cuenta_id,
                    'codigo': str(cuenta_id),
                    'nombre': "",
                    'contacto_id': None,
                    'contacto_nombre': None,                    
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
        
        # Agregar clases, grupos y cuentas al resultado final
        resultados_json.extend(clases_dict.values())
        resultados_json.extend(grupos_dict.values())
        resultados_json.extend(cuentas_dict.values())
        resultados_json.sort(key=lambda x: str(x['codigo']))
        return resultados_json

    def obtener_balance_prueba_tercero(self, fecha_desde, fecha_hasta, cierre = False):
        parametro_cierre = ' AND ma.cierre = false '
        if cierre == True:
            parametro_cierre = ''
            
        query = f'''
            SELECT
                MIN(m.id) AS id,
                m.cuenta_id,    
                c.codigo,
                c.nombre,
                m.contacto_id,
                co.nombre_corto,
                c.cuenta_clase_id,
                c.cuenta_grupo_id,
                c.cuenta_cuenta_id,
                c.nivel,   
                COALESCE((SELECT SUM(debito) FROM con_movimiento ma WHERE ma.cuenta_id = m.cuenta_id AND ma.contacto_id = m.contacto_id and ma.fecha < '{fecha_desde}'), 0) AS debito_anterior,
                COALESCE((SELECT SUM(credito) FROM con_movimiento ma WHERE ma.cuenta_id = m.cuenta_id AND ma.contacto_id = m.contacto_id and ma.fecha < '{fecha_desde}'), 0) AS credito_anterior,
                COALESCE((SELECT SUM(debito) FROM con_movimiento ma WHERE ma.cuenta_id = m.cuenta_id AND ma.contacto_id = m.contacto_id {parametro_cierre} and ma.fecha BETWEEN '{fecha_desde}' AND '{fecha_hasta}'), 0) AS debito,
                COALESCE((SELECT SUM(credito) FROM con_movimiento ma WHERE ma.cuenta_id = m.cuenta_id AND ma.contacto_id = m.contacto_id {parametro_cierre} and ma.fecha BETWEEN '{fecha_desde}' AND '{fecha_hasta}'), 0) AS credito
            FROM
                con_movimiento m
            LEFT JOIN
                con_cuenta c ON m.cuenta_id = c.id
            LEFT JOIN
                gen_contacto co ON m.contacto_id = co.id  
            WHERE 
                m.fecha <= '{fecha_hasta}' and m.contacto_id is not null   
            GROUP BY
                m.cuenta_id, m.contacto_id, co.nombre_corto, c.codigo, c.nombre, c.cuenta_clase_id, c.cuenta_grupo_id, c.cuenta_cuenta_id, c.nivel
            ORDER BY
                c.cuenta_clase_id,
                c.cuenta_grupo_id,
                c.cuenta_cuenta_id;
        '''
        resultados = ConMovimiento.objects.raw(query)
        
        # Procesar resultados
        resultados_json = []        
        for cuenta in resultados:
            saldo_anterior = cuenta.debito_anterior - cuenta.credito_anterior
            saldo_actual = saldo_anterior + (cuenta.debito - cuenta.credito)
            resultados_json.append({
                'tipo': 'TERCERO',
                'cuenta_id': cuenta.cuenta_id,
                'codigo': cuenta.codigo,
                'nombre': cuenta.nombre,
                'contacto_id': cuenta.contacto_id,
                'contacto_nombre': cuenta.nombre_corto,
                'cuenta_clase_id': cuenta.cuenta_clase_id,
                'cuenta_grupo_id': cuenta.cuenta_grupo_id,
                'cuenta_cuenta_id': cuenta.cuenta_cuenta_id,
                'nivel': cuenta.nivel,
                'saldo_anterior': saldo_anterior,
                'debito': cuenta.debito,
                'credito': cuenta.credito,
                'saldo_actual': saldo_actual
            })                                        
        #resultados_json.sort(key=lambda x: str(x['codigo']))
        return resultados_json

    @action(detail=False, methods=["post"], url_path=r'informe-balance-prueba',)
    def informe_balance_prueba(self, request):    
        raw = request.data
        filtros = raw.get("filtros", [])
        excel = raw.get('excel', False)
        pdf = raw.get('pdf', False)
        fecha_desde = None
        fecha_hasta = None
        cierre = False        
        for filtro in filtros:
            if filtro["propiedad"] == "fecha_desde":
                fecha_desde = filtro["valor1"]
            if filtro["propiedad"] == "fecha_hasta":
                fecha_hasta = filtro["valor1"]
            if filtro["propiedad"] == "cierre":
                cierre = filtro["valor1"]                
        
        if not fecha_desde or not fecha_hasta:
            return Response(
                {"error": "Los filtros 'fecha_desde' y 'fecha_hasta' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        resultados_json = self.obtener_balance_prueba(fecha_desde, fecha_hasta, cierre)
        if pdf:
            formato = FormatoBalancePrueba()
            pdf = formato.generar_pdf(id, fecha_desde, fecha_hasta, resultados_json)
            nombre_archivo = f"balance_prueba{fecha_desde}.pdf"
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
        if excel:
            wb = Workbook()
            ws = wb.active
            ws.title = "Balance de prueba"
            headers = ["TIPO", "CUENTA", "NOMBRE CUENTA", "ANTERIOR", "DEBITO", "CREDITO", "ACTUAL"]
            ws.append(headers)
            for registro in resultados_json:
                ws.append([
                    registro['tipo'],
                    registro['codigo'],
                    registro['nombre'],                    
                    registro['saldo_anterior'],
                    registro['debito'],
                    registro['credito'],
                    registro['saldo_actual']
                ])    
            
            estilos_excel = WorkbookEstilos(wb)
            estilos_excel.aplicar_estilos([4,5,6,7])                                
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response['Content-Disposition'] = f'attachment; filename=balance_prueba.xlsx'
            wb.save(response)
            return response
        else:
            return Response({'registros': resultados_json}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path=r'informe-balance-prueba-tercero',)
    def informe_balance_prueba_tercero(self, request):    
        raw = request.data
        filtros = raw.get("filtros", [])
        excel = raw.get('excel', False)
        fecha_desde = None
        fecha_hasta = None
        cierre = False        
        for filtro in filtros:
            if filtro["propiedad"] == "fecha_desde":
                fecha_desde = filtro["valor1"]
            if filtro["propiedad"] == "fecha_hasta":
                fecha_hasta = filtro["valor1"]
            if filtro["propiedad"] == "cierre":
                cierre = filtro["valor1"]                
        
        if not fecha_desde or not fecha_hasta:
            return Response(
                {"error": "Los filtros 'fecha_desde' y 'fecha_hasta' son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        resultados_cuenta = self.obtener_balance_prueba(fecha_desde, fecha_hasta, cierre)
        resultados_tercero = self.obtener_balance_prueba_tercero(fecha_desde, fecha_hasta, cierre)
        resultados = resultados_cuenta + resultados_tercero
        resultados.sort(key=lambda x: str(x['codigo']))
        if excel:
            wb = Workbook()
            ws = wb.active
            ws.title = "Balance de prueba tercero"
            headers = ["TIPO", "CUENTA", "NOMBRE CUENTA", "CONTACTO", "ANTERIOR", "DEBITO", "CREDITO", "ACTUAL"]
            ws.append(headers)
            for registro in resultados:
                ws.append([
                    registro['tipo'],
                    registro['codigo'],
                    registro['nombre'],
                    registro['contacto_nombre'],
                    registro['saldo_anterior'],
                    registro['debito'],
                    registro['credito'],
                    registro['saldo_actual']
                ])    
            
            estilos_excel = WorkbookEstilos(wb)
            estilos_excel.aplicar_estilos([5,6,7,8])                                
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response['Content-Disposition'] = f'attachment; filename=balance_prueba_tercero.xlsx'
            wb.save(response)
            return response
        else:
            return Response({'registros': resultados}, status=status.HTTP_200_OK)
