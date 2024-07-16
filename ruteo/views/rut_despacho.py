from rest_framework import viewsets, permissions
from ruteo.models.rut_despacho import RutDespacho
from ruteo.serializers.rut_despacho import RutDespachoSerializador

class RutDespachoViewSet(viewsets.ModelViewSet):
    queryset = RutDespacho.objects.all()
    serializer_class = RutDespachoSerializador
    permission_classes = [permissions.IsAuthenticated]      

               