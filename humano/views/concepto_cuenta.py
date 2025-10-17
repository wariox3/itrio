from rest_framework import viewsets, permissions
from humano.models.concepto_cuenta import HumConceptoCuenta
from humano.serializers.concepto_cuenta import HumConceptoCuentaSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from humano.filters.concepto_cuenta import ConceptoCuentaFilter

class HumConceptoCuentaViewSet(viewsets.ModelViewSet):
    queryset = HumConceptoCuenta.objects.all()
    serializer_class = HumConceptoCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ConceptoCuentaFilter 
    serializadores = {'lista': HumConceptoCuentaSerializador}

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return HumConceptoCuentaSerializador
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
