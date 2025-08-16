from rest_framework import viewsets, permissions, status
from general.models.documento_pago import GenDocumentoPago
from general.models.documento import GenDocumento
from general.serializers.documento_pago import GenDocumentoPagoSerializador
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response

class DocumentoPagoViewSet(viewsets.ModelViewSet):
    queryset = GenDocumentoPago.objects.all()
    serializer_class = GenDocumentoPagoSerializador
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], url_path=r'anular',)
    def anular_action(self, request):        
        raw = request.data
        id = raw.get('id')
        if id:
            try:
                documento_pago = GenDocumentoPago.objects.get(pk=id)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)            
            try:
                documento = GenDocumento.objects.get(pk=documento_pago.documento_id)
            except GenDocumento.DoesNotExist:
                return Response({'mensaje':'El documento no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
                            
            with transaction.atomic():                
                if documento.estado_aprobado == True and documento.estado_contabilizado == False:
                    documento.pago -= documento_pago.pago
                    documento.pendiente += documento_pago.pago
                    documento.save()
                    documento_pago.pago = 0
                    documento_pago.estado_anulado = True
                    documento_pago.save()
                    return Response({'mensaje': 'Se anula el pago con exito'}, status=status.HTTP_200_OK)
                else:
                    return Response({'mensaje':'El documento debe estar aprobado y sin contabilizar', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    