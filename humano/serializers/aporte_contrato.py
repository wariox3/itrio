from rest_framework import serializers
from humano.models.aporte_contrato import HumAporteContrato
from humano.models.aporte import HumAporte
from humano.models.contrato import HumContrato

class HumAporteContratoSerializador(serializers.HyperlinkedModelSerializer):
    aporte = serializers.PrimaryKeyRelatedField(queryset=HumAporte.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumAporteContrato
        fields = ['id', 'dias', 'salario','base_cotizacion', 'aporte', 'contrato']        

    def to_representation(self, instance):    
        contrato_contacto_id = ''        
        contrato_contacto_numero_identificacion = ''
        contrato_contacto_nombre_corto = ''
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_id = instance.contrato.contacto_id
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto          
        return {
            'id': instance.id,
            'dias': instance.dias,
            'salario': instance.salario,
            'base_cotizacion': instance.base_cotizacion,
            'aporte_id': instance.aporte_id,
            'cotrato_id': instance.contrato_id,
            'contrato_contacto_id': contrato_contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto,
        }      

class HumAporteContratoExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumAporteContrato   

    def to_representation(self, instance):         
        return {
            'id': instance.id,
            'dias': instance.dias,
            'salario': instance.salario,
            'base_cotizacion': instance.base_cotizacion,
            'aporte_id': instance.aporte_id,
            'cotrato_id': instance.contrato_id           
        }       