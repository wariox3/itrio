from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from humano.models.hum_programacion import HumProgramacion
from humano.serializers.hum_programacion import HumProgramacionSerializador
from humano.filters.hum_programacion import HumProgramacionFilter

class HumProgramacionViewSet(viewsets.ModelViewSet):
    queryset = HumProgramacion.objects.all()
    serializer_class = HumProgramacionSerializador
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = HumProgramacionFilter
    ordering_fields = ['id']
    ordering = ['id']    