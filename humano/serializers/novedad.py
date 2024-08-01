from rest_framework import serializers
from humano.models.novedad import HumNovedad
from humano.models.contrato import HumContrato

class HumNovedadSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    
    class Meta:
        model = HumNovedad
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'contrato']

    def to_representation(self, instance):      
        contrato_contacto_numero_identificacion = ''
        contrato_contacto_nombre_corto = ''
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto
        }         