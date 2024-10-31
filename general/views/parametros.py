from rest_framework import viewsets, permissions
from general.models.parametros import GenParametros
from general.serializers.parametros import GenParametrosSerializador

class ParametrosViewSet(viewsets.ModelViewSet):
    queryset = GenParametros.objects.all()
    serializer_class = GenParametrosSerializador    
    permission_classes = [permissions.IsAuthenticated]