from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from general.models.regimen import GenRegimen
from general.serializers.regimen import GenRegimenSerializador
from general.filters.regimen import RegimenFilter
from rest_framework.response import Response

class RegimenViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegimenFilter
    queryset = GenRegimen.objects.all()
    serializer_class = GenRegimenSerializador

    def get_queryset(self):
        queryset = super().get_queryset()               
        select_related = getattr(self.serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = self.serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos)     
        return queryset 
        

    @action(detail=False, methods=["get"], url_path=r'seleccionar')
    def seleccionar_action(self, request):
        limit = request.query_params.get('limit', 10)
        nombre = request.query_params.get('nombre__icontains', None)
        inactivo = request.query_params.get('inactivo', None)
        queryset = self.get_queryset()
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        if inactivo:
            queryset = queryset.filter(inactivo=inactivo)
        try:
            limit = int(limit)
            queryset = queryset[:limit]
        except ValueError:
            pass    
        serializer = self.get_serializer(queryset, many=True)        
        return Response(serializer.data)   