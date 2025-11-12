from rest_framework import serializers
from vertical.models.verificacion import VerVerificacion

class VerVerficacionSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerVerificacion
        fields = ['id', 'fecha_registro', 'verificacion_tipo_id','verificador', 'vehiculo', 'conductor']