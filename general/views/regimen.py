from rest_framework import viewsets, permissions
from general.models.regimen import GenRegimen
from general.serializers.regimen import GenRegimenSerializador

class RegimenViewSet(viewsets.ModelViewSet):
    queryset = GenRegimen.objects.all()
    serializer_class = GenRegimenSerializador
    permission_classes = [permissions.IsAuthenticated]