from rest_framework import viewsets
from inquilino.serializers.verificacion import VerificacionSerializer
from inquilino.models import Verificacion

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = Verificacion.objects.all()
    serializer_class = VerificacionSerializer