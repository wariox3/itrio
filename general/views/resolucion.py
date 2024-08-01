from rest_framework import viewsets, permissions
from general.models.resolucion import Resolucion
from general.serializers.resolucion import GenResolucionSerializador

class ResolucionViewSet(viewsets.ModelViewSet):
    queryset = Resolucion.objects.all()
    serializer_class = GenResolucionSerializador
    permission_classes = [permissions.IsAuthenticated]

