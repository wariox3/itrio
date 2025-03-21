from rest_framework import serializers
from general.models.archivo import GenArchivo
from general.models.documento import GenDocumento

class GenArchivoSerializador(serializers.HyperlinkedModelSerializer):          
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), default=None, allow_null=True)    

    class Meta:
        model = GenArchivo
        fields = ['id', 'documento']

    def to_representation(self, instance):        
        return {
            'id': instance.id,
            'fecha': instance.fecha,
            'nombre': instance.nombre,
            'tipo': instance.tipo,
            'tamano': instance.tamano,
            'almacenamiento_id': instance.almacenamiento_id,
            'documento_id': instance.documento_id,
            'uuid': instance.uuid                        
        }