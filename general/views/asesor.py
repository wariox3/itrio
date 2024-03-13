from rest_framework import viewsets, permissions
from general.models.asesor import Asesor
from general.serializers.asesor import AsesorSerializador

class AsesorViewSet(viewsets.ModelViewSet):
    queryset = Asesor.objects.all()
    serializer_class = AsesorSerializador    
    permission_classes = [permissions.IsAuthenticated]               