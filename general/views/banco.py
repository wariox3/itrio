from rest_framework import viewsets, permissions
from general.models.banco import GenBanco
from general.serializers.banco import GenBancoSerializador

class BancoViewSet(viewsets.ModelViewSet):
    queryset = GenBanco.objects.all()
    serializer_class = GenBancoSerializador
    permission_classes = [permissions.IsAuthenticated]