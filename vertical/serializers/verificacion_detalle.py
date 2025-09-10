from rest_framework import serializers
from vertical.models.verificacion_detalle import VerVerificacionDetalle

class VerVerificacionDetalleSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerVerificacionDetalle
        fields = ['id', 'verificado' ,'verificacion', 'verificacion_concepto']