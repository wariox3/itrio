from rest_framework import viewsets, permissions
from general.models.impuesto_tipo import GenImpuestoTipo
from general.serializers.impuesto_tipo import GenImpuestoTipoSerializador

class ImpuestoTipoViewSet(viewsets.ModelViewSet):
    queryset = GenImpuestoTipo.objects.all()
    serializer_class = GenImpuestoTipoSerializador
    permission_classes = [permissions.IsAuthenticated]  