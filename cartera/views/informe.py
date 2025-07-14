from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from django.http import HttpResponse
from utilidades.workbook_estilos_deprecated import WorkbookEstilos
from django.db.models import Sum, F, Value, Subquery, OuterRef, Count, Q
from django.db.models.functions import Coalesce
from decimal import Decimal

class InformeView(APIView):
    permission_classes = (IsAuthenticated,)        

    def get(self, request):    
        
        cantidad_limite = request.query_params.get('cantidad_limite', 30000)
        desplazar = request.query_params.get('desplazar', 0)
        limite = request.query_params.get('limite', 50)
        excel = request.query_params.get('excel', False)                
        fecha_hasta = request.query_params.get('fecha')
        if not fecha_hasta:
            return Response({"mensaje": "El parámetro fecha es obligatorio."},status=status.HTTP_400_BAD_REQUEST)

        documentos = GenDocumento.objects.filter(            
            documento_tipo__cobrar=True,
            estado_aprobado=True,
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
                documento_tipo__nombre=F('documento_tipo__nombre'),
                contacto__numero_identificacion=F('contacto__numero_identificacion'),
                contacto__nombre_corto=F('contacto__nombre_corto')
            ).filter(
                saldo__gt=0
            ).values('id', 'numero', 'fecha', 'fecha_vence', 'documento_tipo_id', 'subtotal', 'impuesto', 'total', 
                     'documento_tipo__nombre', 'contacto__numero_identificacion', 'contacto__nombre_corto',
                     'abono', 'saldo')   
        cantidad_documentos = documentos[:cantidad_limite].count()                                 
        documentos = documentos[desplazar:limite+desplazar]

        resultados = list(documentos)
        if excel:
            wb = Workbook()
            ws = wb.active
            ws.title = "cuentas_cobrar_corte"
            headers = ["ID", "DOCUMENTO", "NUMERO", "FECHA", "VENCE", "NIT", "CONTACTO", "SUBTOTAL", "IMPUESTO", "TOTAL", "ABONO", "PENDIENTE"]
            ws.append(headers)
            for registro in resultados:
                ws.append([
                    registro['id'],
                    registro['documento_tipo__nombre'],
                    registro['numero'],
                    registro['fecha'],
                    registro['fecha_vence'],
                    registro['contacto__numero_identificacion'],
                    registro['contacto__nombre_corto'],
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
            return Response({'registros': resultados, "cantidad_registros": cantidad_documentos}, status=status.HTTP_200_OK) 