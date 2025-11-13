from rest_framework import serializers
from vertical.models.verificacion import VerVerificacion

class VerVerficacionSerializador(serializers.ModelSerializer):
    vehiculo__placa = serializers.CharField(source='vehiculo.placa', read_only=True)
    conductor__numero_identificacion = serializers.CharField(source='conductor.numero_identificacion', read_only=True)
    conductor__nombre_corto = serializers.CharField(source='conductor.nombre_corto', read_only=True)
    class Meta:
        model = VerVerificacion
        fields = ['id', 'fecha_registro', 'verificacion_tipo_id', 'verificador', 'vehiculo', 'vehiculo__placa' ,'conductor', 'conductor__numero_identificacion', 'conductor__nombre_corto' ,'estado_proceso', 'verificado']
        select_related_fields = ['vehiculo', 'conductor']              