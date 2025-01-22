from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from general.models.documento import GenDocumento
from general.models.documento_detalle import GenDocumentoDetalle
from general.serializers.documento import GenDocumentoSerializador
from general.serializers.documento_detalle import GenDocumentoDetalleSerializador, GenDocumentoDetalleInformeSerializador, GenDocumentoDetalleExcelSerializador
from general.serializers.documento_impuesto import GenDocumentoImpuestoSerializador
from utilidades.excel import WorkbookEstilos

from openpyxl import Workbook
class DocumentoDetalleViewSet(viewsets.ModelViewSet):
    queryset = GenDocumentoDetalle.objects.all()
    serializer_class = GenDocumentoDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        raw = request.data
        documentoDetalleSerializador = GenDocumentoDetalleSerializador(data=raw)
        if documentoDetalleSerializador.is_valid():
            documentoDetalleSerializador.save()            
            return Response({'documento': documentoDetalleSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': documentoDetalleSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)     