from rest_framework import viewsets, permissions
from humano.models.grupo import HumGrupo
from humano.serializers.grupo import HumGrupoSerializador
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from humano.filters.grupo import GrupoFilter

class HumGrupoViewSet(viewsets.ModelViewSet):
    queryset = HumGrupo.objects.all()
    serializer_class = HumGrupoSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GrupoFilter 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumGrupoSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 