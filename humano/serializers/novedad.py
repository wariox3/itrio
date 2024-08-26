from rest_framework import serializers
from humano.models.novedad import HumNovedad
from humano.models.novedad_tipo import HumNovedadTipo
from humano.models.contrato import HumContrato

class HumNovedadSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    novedad_tipo = serializers.PrimaryKeyRelatedField(queryset=HumNovedadTipo.objects.all())
    
    class Meta:
        model = HumNovedad
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_desde_periodo', 'fecha_hasta_periodo', 
                  'dias_disfrutados', 'dias_disfrutados_reales', 'dias_dinero', 
                  'pago_disfrute', 'pago_dinero', 'pago_dia_disfrute', 'pago_dia_dinero', 'contrato', 'novedad_tipo']

    def to_representation(self, instance):      
        contrato_contacto_numero_identificacion = ''
        contrato_contacto_nombre_corto = ''
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto
        novedad_tipo_nombre = ''
        if instance.novedad_tipo:
            novedad_tipo_nombre = instance.novedad_tipo.nombre
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'fecha_desde_periodo': instance.fecha_desde_periodo,
            'fecha_hasta_periodo': instance.fecha_hasta_periodo,            
            'dias_disfrutados': instance.dias_disfrutados,
            'dias_disfrutados_reales': instance.dias_disfrutados_reales,
            'dias_dinero': instance.dias_dinero,
            'pago_disfrute': instance.pago_disfrute,
            'pago_dinero': instance.pago_dinero,            
            'pago_dia_disfrute': instance.pago_dia_disfrute,
            'pago_dia_dinero': instance.pago_dia_dinero,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto,
            'novedad_tipo_id': instance.novedad_tipo_id,
            'novedad_tipo_nombre': novedad_tipo_nombre
        }         