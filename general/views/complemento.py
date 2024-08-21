from rest_framework import viewsets, permissions
from general.models.complemento import GenComplemento
from general.serializers.complemento import GenComplementoSerializador

class ComplementoViewSet(viewsets.ModelViewSet):
    queryset = GenComplemento.objects.all()
    serializer_class = GenComplementoSerializador
    permission_classes = [permissions.IsAuthenticated]