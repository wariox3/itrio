from rest_framework import serializers
from humano.models.aporte import HumAporte
from humano.models.sucursal import HumSucursal

class HumAporteSerializador(serializers.HyperlinkedModelSerializer):
    anio = serializers.IntegerField(required=True)
    mes = serializers.IntegerField(required=True)    
    sucursal = serializers.PrimaryKeyRelatedField(queryset=HumSucursal.objects.all())

    class Meta:
        model = HumAporte
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'anio', 'mes', 'anio_salud', 'mes_salud', 'sucursal',
                  'presentacion', 'estado_generado', 'estado_aprobado']      
        
    def to_representation(self, instance):      
        sucursal_nombre = ''
        if instance.sucursal:
            sucursal_nombre = instance.sucursal.nombre    
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'fecha_hasta_periodo': instance.fecha_hasta_periodo,
            'anio': instance.anio,
            'mes': instance.mes,
            'anio_salud': instance.anio_salud,
            'mes_salud': instance.mes_salud,
            'presentacion': instance.presentacion,
            'estado_generado': instance.estado_generado,
            'estado_aprobado': instance.estado_aprobado,
            'sucursal_id': instance.sucursal_id,
            'sucursal_nombre': sucursal_nombre            
        }          