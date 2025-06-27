from rest_framework import serializers
from humano.models.tiempo import HumTiempo


class HumTiempoSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumTiempo
        fields = ['id', 'nombre']

class HumTiempoSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumTiempo
        fields = ['id', 'nombre']

class HumTiempoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumTiempo

    def to_representation(self, instance):
        return {
            'tiempo_id': instance.id,
            'tiempo_nombre': instance.nombre,
        }          