from rest_framework import viewsets, permissions
from general.models.sede import Sede
from general.serializers.sede import GenSedeSerializador

class SedeViewSet(viewsets.ModelViewSet):
    queryset = Sede.objects.all()
    serializer_class = GenSedeSerializador    
    permission_classes = [permissions.IsAuthenticated]               