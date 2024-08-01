from rest_framework import viewsets, permissions
from general.models.documento_pago import DocumentoPago
from general.serializers.documento_pago import GenDocumentoPagoSerializador

class DocumentoPagoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoPago.objects.all()
    serializer_class = GenDocumentoPagoSerializador
    permission_classes = [permissions.IsAuthenticated]