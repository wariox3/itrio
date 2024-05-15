from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from general.models.documento import Documento
from general.models.documento_detalle import DocumentoDetalle
from general.serializers.documento import DocumentoSerializador
from general.serializers.documento_detalle import DocumentoDetalleSerializador, DocumentoDetalleInformeSerializador, DocumentoDetalleExcelSerializador
from general.serializers.documento_impuesto import DocumentoImpuestoSerializador
from utilidades.excel import WorkbookEstilos

from openpyxl import Workbook
class DocumentoDetalleViewSet(viewsets.ModelViewSet):
    queryset = DocumentoDetalle.objects.all()
    serializer_class = DocumentoDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        raw = request.data
        documentoDetalleSerializador = DocumentoDetalleSerializador(data=raw)
        if documentoDetalleSerializador.is_valid():
            documentoDetalleSerializador.save()            
            return Response({'documento': documentoDetalleSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoDetalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'informe',)
    def lista(self, request):
        raw = request.data
        documento_clase_id = raw.get('documento_clase_id')
        if documento_clase_id:
            desplazar = raw.get('desplazar', 0)
            limite = raw.get('limite', 50)    
            limiteTotal = raw.get('limite_total', 5000)                
            ordenamientos = raw.get('ordenamientos', [])            
            ordenamientos.insert(0, 'documento__estado_aprobado')
            ordenamientos.append('documento__numero')
            filtros = raw.get('filtros', [])            
            filtros.append({'propiedad': 'documento__documento_tipo__documento_clase_id', 'valor1': documento_clase_id})        
            respuesta = DocumentoDetalleViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)     
            serializador = DocumentoDetalleInformeSerializador(respuesta['documentos_detalles'], many=True)
            documentos = serializador.data
            return Response(documentos, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
   
    @action(detail=False, methods=["post"], url_path=r'excel',)
    def excel(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 5000)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = raw.get('filtros', [])        
        ordenamientos = raw.get('ordenamientos', [])            
        ordenamientos.insert(0, 'documento__estado_aprobado')
        ordenamientos.append('-documento__numero')        
        documento_clase = raw.get('documento_clase_id')
        if documento_clase:
            filtros.append({'propiedad': 'documento__documento_tipo__documento_clase_id', 'valor1': documento_clase})
            respuesta = DocumentoDetalleViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)
            serializador = DocumentoDetalleExcelSerializador(respuesta['documentos_detalles'], many=True)
            documentos = serializador.data
            field_names = list(documentos[0].keys()) if documentos else []
            wb = Workbook()
            ws = wb.active
            ws.append(field_names)
            for row in documentos:
                row_data = [row[field] for field in field_names]
                ws.append(row_data)

            estilos_excel = WorkbookEstilos(wb)
            estilos_excel.aplicar_estilos()

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response['Content-Disposition'] = 'attachment; filename=informeVentaItem.xlsx'
            wb.save(response)
            return response
        else: 
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        documentoDetalles = DocumentoDetalle.objects.all()
        if filtros:
            for filtro in filtros:
                documentoDetalles = documentoDetalles.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            documentoDetalles = documentoDetalles.order_by(*ordenamientos)              
        documentoDetalles = documentoDetalles[desplazar:limite+desplazar]
        itemsCantidad = Documento.objects.all()[:limiteTotal].count()                   
        respuesta = {'documentos_detalles': documentoDetalles, "cantidad_registros": itemsCantidad}
        return respuesta 