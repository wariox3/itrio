from rest_framework import viewsets, permissions
from general.models.documento_pago import DocumentoPago
from general.serializers.documento_pago import DocumentoPagoSerializador

class DocumentoPagoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoPago.objects.all()
    serializer_class = DocumentoPagoSerializador
    permission_classes = [permissions.IsAuthenticated]