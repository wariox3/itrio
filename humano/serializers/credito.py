from rest_framework import serializers
from humano.models.credito import HumCredito
from humano.models.contrato import HumContrato

class HumCreditoSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumCredito
        fields = ['id', 'fecha_inicio', 'total', 'cuota', 'cantidad_cuotas', 'validar_cuotas', 'contrato']

    def to_representation(self, instance):      
        contrato_contacto_numero_identificacion = ''
        contrato_contacto_nombre_corto = ''
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto
        return {
            'id': instance.id,
            'fecha_inicio': instance.fecha_inicio,
            'total': instance.total,
            'cuota': instance.cuota,            
            'cantidad_cuotas': instance.cantidad_cuotas,
            'validar_cuotas': instance.validar_cuotas,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto
        }         
        