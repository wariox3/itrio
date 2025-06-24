from rest_framework import serializers
from contabilidad.models.periodo import ConPeriodo

class ConPeriodoListaSerializador(serializers.ModelSerializer):          
    class Meta:
        model = ConPeriodo
        fields = ['id', 'anio', 'mes', 'estado_bloqueado', 'estado_cerrado', 'estado_inconsistencia']

#deprecated
class ConPeriodoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConPeriodo
        fields = ['id', 'anio', 'mes', 'estado_bloqueado', 'estado_cerrado', 'estado_inconsistencia']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'anio': instance.anio,
            'mes': instance.mes,
            'estado_bloqueado': instance.estado_bloqueado,
            'estado_cerrado': instance.estado_cerrado,
            'estado_inconsistencia': instance.estado_inconsistencia,
        }        
        