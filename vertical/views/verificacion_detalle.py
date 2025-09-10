from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from vertical.models.verificacion_detalle import VerVerificacionDetalle
from vertical.serializers.verificacion_detalle import VerVerificacionDetalleSerializador
from django.db import transaction

class VerificacionDetalleViewSet(viewsets.ModelViewSet):
    queryset = VerVerificacionDetalle.objects.all()
    serializer_class = VerVerificacionDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]


        
   