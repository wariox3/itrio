from rest_framework import serializers
from humano.models.aporte_entidad import HumAporteEntidad
from humano.models.aporte import HumAporte
from humano.models.entidad import HumEntidad

class HumAporteEntidadSerializador(serializers.HyperlinkedModelSerializer):
    aporte = serializers.PrimaryKeyRelatedField(queryset=HumAporte.objects.all())    
    entidad = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())

    class Meta:
        model = HumAporteEntidad
        fields = ['id', 'aporte', 'tipo', 'cotizacion', 'entidad']        

    def to_representation(self, instance):    
        entidad_nombre = ""
        if instance.entidad:
            entidad_nombre = instance.entidad.nombre
        return {
            'id': instance.id,
            'tipo': instance.tipo,
            'cotizacion': instance.cotizacion,
            'entidad_id': instance.entidad_id,
            'entidad_nombre': entidad_nombre
        }      

class HumAporteEntidadExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumAporteEntidad   

    def to_representation(self, instance): 
        entidad_nombre = ""
        if instance.entidad:
            entidad_nombre = instance.entidad.nombre        
        return {
            'id': instance.id,
            'tipo': instance.tipo,
            'cotizacion': instance.cotizacion,
            'entidad_id': instance.entidad_id,
            'entidad_nombre': entidad_nombre
        }       