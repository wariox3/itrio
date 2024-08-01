from rest_framework import viewsets, permissions
from general.models.documento_pago import GenDocumentoPago
from general.serializers.documento_pago import GenDocumentoPagoSerializador

class DocumentoPagoViewSet(viewsets.ModelViewSet):
    queryset = GenDocumentoPago.objects.all()
    serializer_class = GenDocumentoPagoSerializador
    permission_classes = [permissions.IsAuthenticated]