from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from django.http import HttpResponse
from utilidades.excel import WorkbookEstilos
from django.db.models import Sum, F, Value, Subquery, OuterRef, Count, Q
from django.db.models.functions import Coalesce
from decimal import Decimal

class InformeView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def obtener_pendiente_corte(self, fecha_hasta, filtros, cantidad_limite, desplazar, limite):
        documentos = GenDocumento.objects.filter(            
            documento_tipo__cobrar=True,
            fecha__lte=fecha_hasta
            ).annotate(                
                abono=Coalesce(Sum(
                        'documentos_detalles_documento_afectado_rel__precio',
                        filter=Q(documentos_detalles_documento_afectado_rel__documento__fecha__lte=fecha_hasta)
                    ), Decimal(0)),
                saldo=F('total') - Coalesce(Sum(
                    'documentos_detalles_documento_afectado_rel__precio',
                    filter=Q(documentos_detalles_documento_afectado_rel__documento__fecha__lte=fecha_hasta)
                ), Decimal(0)),
                documento_tipo_nombre=F('documento_tipo__nombre'),
                contacto_numero_identificacion=F('contacto__numero_identificacion'),
                contacto_nombre_corto=F('contacto__nombre_corto')
            ).filter(
                saldo__gt=0
            ).values('id', 'numero', 'fecha', 'fecha_vence', 'documento_tipo_id', 'subtotal', 'impuesto', 'total', 
                     'documento_tipo_nombre', 'contacto_numero_identificacion', 'contacto_nombre_corto',
                     'abono', 'saldo')
        if filtros:
            for filtro in filtros:                    
                if filtro['propiedad'] != 'fecha':
                    operador = filtro.get('operador', None)                
                    if operador:                        
                        if operador == 'range':
                            documentos = documentos.filter(**{filtro['propiedad']+'__'+operador: (filtro['valor1'], filtro['valor2'])})
                        else:
                            documentos = documentos.filter(**{filtro['propiedad']+'__'+operador: filtro['valor1']})
                    else:
                        documentos = documentos.filter(**{filtro['propiedad']: filtro['valor1']})   
        cantidad_documentos = documentos[:cantidad_limite].count()                                 
        documentos = documentos[desplazar:limite+desplazar]
        return {'registros': list(documentos), "cantidad_registros": cantidad_documentos}

    def post(self, request):    
        raw = request.data
        filtros = raw.get("filtros", [])
        cantidad_limite = raw.get('cantidad_limite', 30000)
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)
        excel = raw.get('excel', False)
        pdf = raw.get('pdf', False)        
        fecha_hasta = None
        for filtro in filtros:
            if filtro["propiedad"] == "fecha":
                fecha_hasta = filtro["valor1"]            
            if filtro["propiedad"] == "numero":
                numero = filtro["valor1"]                
        
        if not fecha_hasta:
            return Response(
                {"mensaje": "Los filtros 'fecha' son obligatorios."},status=status.HTTP_400_BAD_REQUEST)               
        resultados = self.obtener_pendiente_corte(fecha_hasta, filtros, cantidad_limite, desplazar, limite)
        if excel:
            wb = Workbook()
            ws = wb.active
            ws.title = "Auxiliar general"
            headers = ["ID", "DOCUMENTO", "NUMERO", "FECHA", "VENCE", "NIT", "CONTACTO", "SUBTOTAL", "IMPUESTO", "TOTAL", "ABONO", "PENDIENTE"]
            ws.append(headers)
            for registro in resultados['registros']:
                ws.append([
                    registro['id'],
                    registro['documento_tipo_nombre'],
                    registro['numero'],
                    registro['fecha'],
                    registro['fecha_vence'],
                    registro['contacto_numero_identificacion'],
                    registro['contacto_nombre_corto'],
                    registro['subtotal'],
                    registro['impuesto'],
                    registro['total'],
                    registro['abono'],
                    registro['saldo'],
                ])    
            
            estilos_excel = WorkbookEstilos(wb)
            estilos_excel.aplicar_estilos([8,9,10,11,12])                                
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response['Content-Disposition'] = f'attachment; filename=cuenta_cobrar_corte.xlsx'
            wb.save(response)
            return response
        else:
            return Response(resultados, status=status.HTTP_200_OK) 