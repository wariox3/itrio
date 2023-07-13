from rest_framework import viewsets
from seguridad.serializers import VerificacionSerializer
from seguridad.models import Verificacion

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = Verificacion.objects.all()
    serializer_class = VerificacionSerializer