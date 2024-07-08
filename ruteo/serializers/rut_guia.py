from rest_framework import serializers
from ruteo.models.rut_guia import RutGuia


class RutGuiaSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutGuia
        fields = ['id', 'guia', 'fecha', 'documento', 'destinatario', 'destinatario_direccion', 'destinatario_telefono', 'destinatario_correo', 'peso', 'volumen']

    def to_representation(self, instance):        
        return {
            'id': instance.id,            
        }
    
