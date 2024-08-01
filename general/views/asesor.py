from rest_framework import viewsets, permissions
from general.models.gen_asesor import GenAsesor
from general.serializers.gen_asesor import GenAsesorSerializador

class AsesorViewSet(viewsets.ModelViewSet):
    queryset = GenAsesor.objects.all()
    serializer_class = GenAsesorSerializador    
    permission_classes = [permissions.IsAuthenticated]               