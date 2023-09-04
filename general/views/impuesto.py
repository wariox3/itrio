from rest_framework import viewsets, permissions
from general.models.impuesto import Impuesto
from general.serializers.impuesto import ImpuestoSerializador

class ImpuestoViewSet(viewsets.ModelViewSet):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializador
    permission_classes = [permissions.IsAuthenticated]  