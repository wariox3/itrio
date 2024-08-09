from rest_framework import serializers
from contabilidad.models.periodo import ConPeriodo

class ConPeriodoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConPeriodo
        fields = ['id', 'anio', 'mes']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'anio': instance.anio,
            'mes': instance.mes
        }        
        