from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from general.models.asesor import GenAsesor
from general.serializers.asesor import GenAsesorSerializador
from utilidades.excel_exportar import ExcelExportar
from general.filters.asesor import AsesorFilter
from rest_framework.response import Response

class AsesorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [DjangoFilterBackend]
    filterset_class = AsesorFilter
    queryset = GenAsesor.objects.all()
    serializer_class = GenAsesorSerializador
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()               
        select_related = getattr(self.serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = self.serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos)     
        return queryset 
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        limit = request.query_params.get('limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)          