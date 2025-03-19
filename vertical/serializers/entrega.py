from rest_framework import serializers
from vertical.models.entrega import VerEntrega

class VerEntregaSerializador(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = VerEntrega
        fields = ['id', 'contenedor_id', 'usuario_id']


    def to_representation(self, instance):

        return {
            'id': instance.id,
            'contenedor_id':instance.contenedor_id,
            'usuario_id':instance.usuario_id
        }             
        