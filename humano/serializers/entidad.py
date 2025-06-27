from rest_framework import serializers
from humano.models.entidad import HumEntidad

class HumEntidadSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumEntidad
        fields = ['id', 'nombre']

class HumEntidadSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumEntidad
        fields = ['id', 'codigo', 'numero_identificacion', 'nombre', 'nombre_extendido', 'salud', 'pension', 'cesantias', 'caja',
                  'riesgo', 'sena', 'icbf']

    

class HumEntidadListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumEntidad
    def to_representation(self, instance):
        return {
            'entidad_id': instance.id,
            'entidad_nombre': instance.nombre,
        }         
        