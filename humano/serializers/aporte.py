from rest_framework import serializers
from humano.models.aporte import HumAporte
from humano.models.sucursal import HumSucursal
from humano.models.entidad import HumEntidad

class HumAporteSerializador(serializers.HyperlinkedModelSerializer):
    anio = serializers.IntegerField(required=True)
    mes = serializers.IntegerField(required=True)    
    sucursal = serializers.PrimaryKeyRelatedField(queryset=HumSucursal.objects.all())
    entidad_riesgo = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumAporte
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'anio', 'mes', 'anio_salud', 'mes_salud', 'sucursal',
                  'presentacion', 'estado_generado', 'estado_aprobado', 'entidad_riesgo']      
        
    def to_representation(self, instance):      
        sucursal_nombre = ''
        if instance.sucursal:
            sucursal_nombre = instance.sucursal.nombre    
        entidad_riesgo_nombre = ''
        if instance.entidad_riesgo:
            entidad_riesgo_nombre = instance.entidad_riesgo.nombre        
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
            'sucursal_nombre': sucursal_nombre,
            'entidad_riesgo_id': instance.entidad_riesgo_id,
            'entidad_riesgo_nombre': entidad_riesgo_nombre,            
        }          