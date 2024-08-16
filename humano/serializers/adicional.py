from rest_framework import serializers
from humano.models.adicional import HumAdicional
from humano.models.contrato import HumContrato
from humano.models.concepto import HumConcepto
from humano.models.programacion import HumProgramacion

class HumAdicionalSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    programacion = serializers.PrimaryKeyRelatedField(queryset=HumProgramacion.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumAdicional
        fields = ['id', 'valor', 'horas', 'aplica_dia_laborado', 'detalle', 'concepto', 'contrato', 'programacion', 'permanente',
                  'inactivo', 'inactivo_periodo']

    def to_representation(self, instance):      
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        contrato_contacto_numero_identificacion = ''
        contrato_contacto_nombre_corto = ''
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto
        return {
            'id': instance.id,
            'valor': instance.valor,
            'horas': instance.horas,
            'aplica_dia_laborado': instance.aplica_dia_laborado, 
            'permanente': instance.permanente,
            'inactivo': instance.inactivo,
            'inactivo_periodo': instance.inactivo_periodo,           
            'detalle': instance.detalle,
            'concepto_id': instance.concepto_id,
            'concepto_nombre': concepto_nombre,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto
        }         