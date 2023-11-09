from rest_framework import viewsets, permissions
from general.models.resolucion import Resolucion
from general.serializers.resolucion import ResolucionSerializador

class ResolucionViewSet(viewsets.ModelViewSet):
    queryset = Resolucion.objects.all()
    serializer_class = ResolucionSerializador
    permission_classes = [permissions.IsAuthenticated]

