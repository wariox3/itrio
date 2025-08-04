from rest_framework import serializers
from humano.models.aporte_entidad import HumAporteEntidad
from humano.models.aporte import HumAporte
from humano.models.entidad import HumEntidad

class HumAporteEntidadSerializador(serializers.ModelSerializer):
    entidad__nombre = serializers.CharField(source='entidad.nombre', read_only=True)

    class Meta:
        model = HumAporteEntidad
        fields = ['id', 'tipo', 'cotizacion', 'entidad', 'entidad__nombre', 'aporte']      
        select_related_fields = ['entidad']    


class HumAporteEntidadInformeSerializador(serializers.ModelSerializer):
    entidad__nombre = serializers.CharField(source='entidad.nombre', read_only=True)
    class Meta:
        model = HumAporteEntidad   
        fields = ['id', 'tipo', 'cotizacion', 'entidad', 'entidad__nombre']      
        select_related_fields = ['entidad']
 