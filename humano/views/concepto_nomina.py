from rest_framework import viewsets, permissions
from humano.models.concepto_nomina import HumConceptoNomina
from humano.serializers.concepto_nomina import HumConceptoNominaSerializador

class HumConceptoNominaViewSet(viewsets.ModelViewSet):
    queryset = HumConceptoNomina.objects.all()
    serializer_class = HumConceptoNominaSerializador
    permission_classes = [permissions.IsAuthenticated]