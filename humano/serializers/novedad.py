from rest_framework import serializers
from humano.models.novedad import HumNovedad
from humano.models.novedad_tipo import HumNovedadTipo
from humano.models.contrato import HumContrato

class HumNovedadSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    novedad_tipo = serializers.PrimaryKeyRelatedField(queryset=HumNovedadTipo.objects.all())
    novedad_referencia = serializers.PrimaryKeyRelatedField(queryset=HumNovedad.objects.all(), required=False, allow_null=True)    
    class Meta:
        model = HumNovedad
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_desde_periodo', 'fecha_hasta_periodo', 'fecha_desde_empresa', 'fecha_hasta_empresa',
                  'fecha_desde_entidad', 'fecha_hasta_entidad',
                  'dias_disfrutados', 'dias_disfrutados_reales', 'dias_dinero', 'dias', 'dias_empresa', 'dias_entidad',
                  'pago_disfrute', 'pago_dinero', 'pago_dia_disfrute', 'pago_dia_dinero', 
                  'base_cotizacion_propuesto', 'base_cotizacion', 'hora_empresa', 'hora_entidad', 'pago_empresa', 'pago_entidad',
                  'total', 'contrato', 'novedad_tipo', 'novedad_referencia', 'prorroga']

    def validate(self, data):
        fecha_desde = data.get('fecha_desde')
        fecha_hasta = data.get('fecha_hasta') 
        contrato_id = data.get('contrato_id')       
        novedades = HumNovedad.objects.filter(
            fecha_desde__lte=fecha_hasta,
            fecha_hasta__gte=fecha_desde,
            contrato_id=contrato_id
        )

        if self.instance:
            novedades = novedades.exclude(pk=self.instance.pk)

        if novedades.exists():
            raise serializers.ValidationError("Las fechas se cruzan con otra novedad existente.")

        return data

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
            'fecha_desde_empresa': instance.fecha_desde_empresa,
            'fecha_hasta_empresa': instance.fecha_hasta_empresa,
            'fecha_desde_entidad': instance.fecha_desde_entidad,
            'fecha_hasta_entidad': instance.fecha_hasta_entidad,      
            'dias_disfrutados': instance.dias_disfrutados,
            'dias_disfrutados_reales': instance.dias_disfrutados_reales,
            'dias_dinero': instance.dias_dinero,
            'dias': instance.dias,
            'dias_empresa': instance.dias_empresa,
            'dias_entidad': instance.dias_entidad,
            'pago_disfrute': instance.pago_disfrute,
            'pago_dinero': instance.pago_dinero,            
            'pago_dia_disfrute': instance.pago_dia_disfrute,
            'pago_dia_dinero': instance.pago_dia_dinero,
            'base_cotizacion_propuesto': instance.base_cotizacion_propuesto ,
            'base_cotizacion': instance.base_cotizacion ,
            'hora_empresa': instance.hora_empresa ,
            'hora_entidad': instance.hora_entidad ,
            'pago_empresa': instance.pago_empresa ,
            'pago_entidad': instance.pago_entidad ,
            'total': instance.total,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto,
            'novedad_tipo_id': instance.novedad_tipo_id,
            'novedad_tipo_nombre': novedad_tipo_nombre,
            'novedad_referencia_id' : instance.novedad_referencia_id,
            'prroroga' : instance.prorroga
        }         
    
class HumNovedadSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumNovedad
        fields = ['id']