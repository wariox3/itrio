from rest_framework import serializers
from vertical.models.verificacion_concepto import VerVerificacionConcepto

class VerVerificacionConceptoSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerVerificacionConcepto
        fields = ['id', 'tipo' ,'nombre']