from rest_framework import viewsets, permissions
from general.models.impuesto import Impuesto
from general.serializers.impuesto import ImpuestoSerializer

class ImpuestoViewSet(viewsets.ModelViewSet):
    queryset = Impuesto.objects.all()
    serializer_class = ImpuestoSerializer
    permission_classes = [permissions.IsAuthenticated]