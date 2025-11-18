from rest_framework import serializers
from vertical.models.verificacion_detalle import VerVerificacionDetalle

class VerVerificacionDetalleSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerVerificacionDetalle
        fields = ['id','fecha_verificacion' ,'verificado' ,'verificacion', 'verificacion_concepto']