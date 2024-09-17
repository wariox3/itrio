from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from importlib import import_module
from openpyxl import Workbook
from django.http import HttpResponse
from utilidades.excel import WorkbookEstilos
import re


class ListaView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        modelo_nombre = raw.get('modelo')
        serializador_parametro = raw.get('serializador', '')
        excel = raw.get('excel', False)
        if modelo_nombre:
            aplicacion_prefijo = modelo_nombre[:3].lower()
            modelo_serializado_nombre = modelo_nombre[3:]        
            aplicaciones = {
                'gen': 'general',
                'hum': 'humano',
                'con': 'contabilidad',
                'ven': 'venta',
                'inv': 'inventario',
                'tte': 'transporte',
                'rut': 'ruteo',
            }
            aplicacion = aplicaciones.get(aplicacion_prefijo)
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', modelo_serializado_nombre)                        
            serializador_nombre = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()            
            modulo = import_module(f'{aplicacion}.serializers.{serializador_nombre}')            
            modelo = apps.get_model(aplicacion, modelo_nombre)
            serializador = getattr(modulo, f'{modelo_nombre}{serializador_parametro}Serializador')

            desplazar = raw.get('desplazar', 0)
            limite = raw.get('limite', 50)    
            cantidadLimite = raw.get('cantidad_limite', 5000)    
            filtros = raw.get('filtros')
            ordenamientos = raw.get('ordenamientos')
            items = modelo.objects.all()
            print(items.query)
            if filtros:
                for filtro in filtros:
                    items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if ordenamientos:
                items = items.order_by(*ordenamientos)              
            items = items[desplazar:limite+desplazar]
            itemsCantidad = modelo.objects.all()[:cantidadLimite].count()
            serializadorDatos = serializador(items, many=True) 
            if excel:
                data = serializadorDatos.data
                field_names = list(data[0].keys()) if data else []
                wb = Workbook()
                ws = wb.active
                ws.append(field_names)
                for row in data:
                    row_data = [row[field] for field in field_names]
                    ws.append(row_data)

                estilos_excel = WorkbookEstilos(wb)
                estilos_excel.aplicar_estilos()
                if serializador_parametro:
                    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', serializador_parametro)                        
                    serializador_parametro = "_" + re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()            
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = f'attachment; filename={serializador_nombre}{serializador_parametro}.xlsx'
                wb.save(response)
                return response
            else:
                return Response({"registros": serializadorDatos.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)