from rest_framework import viewsets
from contenedor.serializers.verificacion import VerificacionSerializador
from contenedor.models import Verificacion

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = Verificacion.objects.all()
    serializer_class = VerificacionSerializador