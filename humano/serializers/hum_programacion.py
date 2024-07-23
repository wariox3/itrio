from rest_framework import serializers
from humano.models.hum_programacion import HumProgramacion
from humano.models.hum_grupo import HumGrupo
from humano.models.hum_pago_tipo import HumPagoTipo

class HumProgramacionSerializador(serializers.HyperlinkedModelSerializer):
    pago_tipo = serializers.PrimaryKeyRelatedField(queryset=HumPagoTipo.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all())

    class Meta:
        model = HumProgramacion
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'nombre', 'grupo', 'pago_tipo']
        