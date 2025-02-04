from rest_framework import serializers
from humano.models.aporte import HumAporte
from humano.models.sucursal import HumSucursal
from humano.models.entidad import HumEntidad

class HumAporteSerializador(serializers.HyperlinkedModelSerializer):
    anio = serializers.IntegerField(required=True)
    mes = serializers.IntegerField(required=True)    
    sucursal = serializers.PrimaryKeyRelatedField(queryset=HumSucursal.objects.all())
    entidad_riesgo = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)
    entidad_sena = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)
    entidad_icbf = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumAporte
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'anio', 'mes', 'anio_salud', 'mes_salud', 'sucursal',
                  'presentacion', 'estado_generado', 'estado_aprobado', 'entidad_riesgo', 'entidad_sena', 'entidad_icbf',
                  'cotizacion_pension', 'cotizacion_voluntario_pension_afiliado',
                  'cotizacion_voluntario_pension_aportante', 'cotizacion_solidaridad_solidaridad', 'cotizacion_solidaridad_subsistencia',
                  'cotizacion_salud', 'cotizacion_riesgos', 'cotizacion_caja', 'cotizacion_sena', 'cotizacion_icbf', 'cotizacion_total',
                  'contratos', 'empleados', 'lineas']      

    def to_representation(self, instance):      
        sucursal_nombre = ''
        if instance.sucursal:
            sucursal_nombre = instance.sucursal.nombre    
        entidad_riesgo_nombre = ''
        if instance.entidad_riesgo:
            entidad_riesgo_nombre = instance.entidad_riesgo.nombre  
        entidad_sena_nombre = ''
        if instance.entidad_sena:
            entidad_sena_nombre = instance.entidad_sena.nombre                   
        entidad_icbf_nombre = ''
        if instance.entidad_icbf:
            entidad_icbf_nombre = instance.entidad_icbf.nombre             
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
            'base_cotizacion': instance.base_cotizacion,
            'cotizacion_pension': instance.cotizacion_pension,
            'cotizacion_voluntario_pension_afiliado': instance.cotizacion_voluntario_pension_afiliado,
            'cotizacion_voluntario_pension_aportante': instance.cotizacion_voluntario_pension_aportante,
            'cotizacion_solidaridad_solidaridad': instance.cotizacion_solidaridad_solidaridad,
            'cotizacion_solidaridad_subsistencia': instance.cotizacion_solidaridad_subsistencia,
            'cotizacion_salud': instance.cotizacion_salud,
            'cotizacion_riesgos': instance.cotizacion_riesgos,
            'cotizacion_caja': instance.cotizacion_caja,
            'cotizacion_sena': instance.cotizacion_sena,
            'cotizacion_icbf': instance.cotizacion_icbf,
            'cotizacion_total': instance.cotizacion_total,
            'contratos': instance.contratos,
            'empleados': instance.empleados,
            'lineas': instance.lineas,
            'sucursal_id': instance.sucursal_id,
            'sucursal_nombre': sucursal_nombre,
            'entidad_riesgo_id': instance.entidad_riesgo_id,
            'entidad_riesgo_nombre': entidad_riesgo_nombre, 
            'entidad_sena_id': instance.entidad_sena_id,
            'entidad_sena_nombre': entidad_sena_nombre,                       
            'entidad_icbf_id': instance.entidad_icbf_id,
            'entidad_icbf_nombre': entidad_icbf_nombre
        }          