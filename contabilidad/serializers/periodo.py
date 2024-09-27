from rest_framework import serializers
from contabilidad.models.periodo import ConPeriodo

class ConPeriodoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConPeriodo
        fields = ['id', 'anio', 'mes', 'estado_bloqueado', 'estado_cerrado']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'anio': instance.anio,
            'mes': instance.mes,
            'estado_bloqueado': instance.estado_bloqueado,
            'estado_cerrado': instance.estado_cerrado
        }        
        