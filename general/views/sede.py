from rest_framework import viewsets, permissions
from general.models.sede import GenSede
from general.serializers.sede import GenSedeSerializador

class SedeViewSet(viewsets.ModelViewSet):
    queryset = GenSede.objects.all()
    serializer_class = GenSedeSerializador    
    permission_classes = [permissions.IsAuthenticated]               