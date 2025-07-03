from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from humano.models.configuracion_provision import HumConfiguracionProvision
from humano.serializers.configuracion_provision import HumConfiguracionProvisionSerializador
from humano.filters.configuracion_provision import ConfiguracionProvisionFilter
from rest_framework.pagination import PageNumberPagination

class HumConfiguracionProvisionViewSet(viewsets.ModelViewSet):
    queryset = HumConfiguracionProvision.objects.all()
    serializer_class = HumConfiguracionProvisionSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConfiguracionProvisionFilter   

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumConfiguracionProvisionSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        page_size = self.request.query_params.get('page_size')
        if page_size:
            if page_size != '0':
                self.pagination_class = PageNumberPagination
                self.pagination_class.page_size = int(page_size)
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 