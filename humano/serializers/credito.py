from rest_framework import serializers
from humano.models.credito import HumCredito
from humano.models.contrato import HumContrato
from humano.models.concepto import HumConcepto

class HumCreditoSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumCredito
        fields = ['id', 'fecha_inicio', 'total', 'cuota', 'abono', 'saldo', 'cantidad_cuotas', 'cuota_actual', 'validar_cuotas', 'contrato', 'concepto']

    def to_representation(self, instance):      
        contrato_contacto_numero_identificacion = ''
        contrato_contacto_nombre_corto = ''
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        return {
            'id': instance.id,
            'fecha_inicio': instance.fecha_inicio,
            'total': instance.total,
            'abono': instance.abono,
            'saldo': instance.saldo,
            'cuota': instance.cuota,
            'cantidad_cuotas': instance.cantidad_cuotas,
            'cuota_actual': instance.cuota_actual,
            'validar_cuotas': instance.validar_cuotas,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto,
            'concepto_id': instance.concepto_id,
            'concepto_nombre': concepto_nombre,
            'inactivo': instance.inactivo,
            'inactivo_periodo': instance.inactivo_periodo
        }         
        