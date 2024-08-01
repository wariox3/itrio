from rest_framework import viewsets, permissions
from humano.models.adicional import HumAdicional
from humano.serializers.adicional import HumAdicionalSerializador

class HumAdicionalViewSet(viewsets.ModelViewSet):
    queryset = HumAdicional.objects.all()
    serializer_class = HumAdicionalSerializador
    permission_classes = [permissions.IsAuthenticated]