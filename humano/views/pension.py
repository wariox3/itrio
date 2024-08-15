from rest_framework import viewsets, permissions
from humano.models.pension import HumPension
from humano.serializers.pension import HumPensionSerializador

class HumPensionViewSet(viewsets.ModelViewSet):
    queryset = HumPension.objects.all()
    serializer_class = HumPensionSerializador
    permission_classes = [permissions.IsAuthenticated]