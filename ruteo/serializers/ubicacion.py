from rest_framework import serializers
from ruteo.models.ubicacion import RutUbicacion
from ruteo.models.despacho import RutDespacho
from ruteo.models.visita import RutVisita

class RutUbicacionSerializador(serializers.HyperlinkedModelSerializer):    
    despacho = serializers.PrimaryKeyRelatedField(queryset=RutDespacho.objects.all(), default=None, allow_null=True)
    visita = serializers.PrimaryKeyRelatedField(queryset=RutVisita.objects.all(), default=None, allow_null=True)
    
    class Meta:
        model = RutUbicacion
        fields = ['id', 'fecha', 'latitud', 'longitud', 'despacho', 'visita']

    def to_representation(self, instance):      
        return {
            'id': instance.id,  
            'fecha': instance.fecha,
            'latitud': instance.latitud,
            'longitud': instance.longitud
        }