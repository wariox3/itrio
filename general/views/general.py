from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from general.models.documento import GenDocumento
from general.formatos.nomina import FormatoNomina
from general.formatos.factura import FormatoFactura
from django.apps import apps
from importlib import import_module
from openpyxl import Workbook
from django.http import HttpResponse
from utilidades.workbook_estilos import WorkbookEstilos
import re
import zipfile
import io
from datetime import datetime

class ListaView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        raw = request.data
        modelo_nombre = raw.get('modelo')
        serializador_parametro = raw.get('serializador', '')
        excel = raw.get('excel', False)
        zip = raw.get('zip', False)
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
            if excel:   
                limite = 30000    
            cantidadLimite = raw.get('cantidad_limite', 30000)    
            filtros = raw.get('filtros')
            exclusiones = raw.get('exclusiones')
            ordenamientos = raw.get('ordenamientos')
            items = modelo.objects.all()            
            if filtros:
                for filtro in filtros:                    
                    operador = filtro.get('operador', None)
                    if operador:
                        if operador == 'range':
                            items = items.filter(**{filtro['propiedad']+'__'+operador: (filtro['valor1'], filtro['valor2'])})
                        elif operador == 'in':                                    
                            valores = filtro['valor1'] if isinstance(filtro['valor1'], list) else [filtro['valor1']]     
                            items = items.filter(**{filtro['propiedad']+'__'+operador: valores})                      
                        else:
                            items = items.filter(**{filtro['propiedad']+'__'+operador: filtro['valor1']})
                    else:
                        items = items.filter(**{filtro['propiedad']: filtro['valor1']})
            if exclusiones:
                for exclusion in exclusiones:                    
                    operador = exclusion.get('operador', None)
                    if operador:
                        if operador == 'range':
                            items = items.exclude(**{exclusion['propiedad']+'__'+operador: (exclusion['valor1'], exclusion['valor2'])})
                        else:
                            items = items.exclude(**{exclusion['propiedad']+'__'+operador: exclusion['valor1']})
                    else:
                        items = items.exclude(**{exclusion['propiedad']: exclusion['valor1']})      
            #print(items.query)                        
            itemsCantidad = items[:cantidadLimite].count()
            if ordenamientos:
                items = items.order_by(*ordenamientos)              
            items = items[desplazar:limite+desplazar]             
            #itemsCantidad = modelo.objects.all()[:cantidadLimite].count()
            serializadorDatos = serializador(items, many=True) 
            if excel:
                data = serializadorDatos.data
                field_names = list(data[0].keys()) if data else []
                wb = Workbook()
                ws = wb.active
                ws.append(field_names)
                for row in data:
                    #row_data = [row[field] for field in field_names]
                    row_data = []
                    for field in field_names:
                        value = row.get(field)
                        if value is None:
                            row_data.append("")
                        elif isinstance(value, datetime) and value.tzinfo is not None:
                            row_data.append(value.replace(tzinfo=None))
                        else:
                            row_data.append(value)
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
            
            if zip:
                data = serializadorDatos.data                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for index, record in enumerate(data):
                        id = record.pop('id', None)
                        pdf_bytes = None
                        documento = GenDocumento.objects.get(pk=id)                        
                        if documento.documento_tipo_id in (1,2,3):                                        
                            formato = FormatoFactura()
                            pdf_bytes = formato.generar_pdf(id)                                          
                            nombres_archivo = {
                                100: f"factura_{id}_{documento.numero}.pdf" if documento.numero else f"Factura_{id}.pdf",
                                101: f"notaCredito_{id}_{documento.numero}.pdf" if documento.numero else f"NotaCredito_{id}.pdf",
                                102: f"notaDebito_{id}_{documento.numero}.pdf" if documento.numero else f"NotaDebito_{id}.pdf"
                            }
                            nombre_archivo = nombres_archivo.get(documento.documento_tipo.documento_clase.id)
                        
                        if documento.documento_tipo_id == 14:
                            formato = FormatoNomina()
                            pdf_bytes = formato.generar_pdf(id)              
                            nombre_archivo = f"nomina_{id}.pdf"                    
                        zip_file.writestr(nombre_archivo, pdf_bytes)                         
                zip_buffer.seek(0)
                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = f'attachment; filename="{modelo_serializado_nombre.lower()}.zip"'
                return response
            else:
                return Response({"registros": serializadorDatos.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)