from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.serializers.programacion_detalle import HumProgramacionDetalleSerializador

class HumProgramacionDetalleViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacionDetalle.objects.all()
    serializer_class = HumProgramacionDetalleSerializador
    permission_classes = [permissions.IsAuthenticated]       