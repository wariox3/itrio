from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.verificacion import VerVerificacion
from vertical.serializers.verificacion import VerVerficacionSerializador
from django.db import transaction

class VerificacionViewSet(viewsets.ModelViewSet):
    queryset = VerVerificacion.objects.all()
    serializer_class = VerVerficacionSerializador
    permission_classes = [permissions.IsAuthenticated]


        
   