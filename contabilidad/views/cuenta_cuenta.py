from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta
from contabilidad.serializers.cuenta_cuenta import ConCuentaCuentaSerializador
from contabilidad.filters.cuenta_cuenta import CuentaCuentaFilter

class CuentaCuentaViewSet(viewsets.ModelViewSet):
    queryset = ConCuentaCuenta.objects.all()
    serializer_class = ConCuentaCuentaSerializador
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CuentaCuentaFilter 

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return ConCuentaCuentaSerializador
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