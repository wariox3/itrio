from rest_framework import viewsets, permissions
from humano.models.hum_concepto import HumConcepto
from humano.serializers.hum_concepto import HumConceptoSerializador

class HumConceptoViewSet(viewsets.ModelViewSet):
    queryset = HumConcepto.objects.all()
    serializer_class = HumConceptoSerializador
    permission_classes = [permissions.IsAuthenticated]