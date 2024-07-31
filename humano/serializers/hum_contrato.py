from rest_framework import serializers
from general.models.contacto import Contacto
from humano.models.hum_contrato import HumContrato
from humano.models.hum_contrato_tipo import HumContratoTipo
from humano.models.hum_grupo import HumGrupo

class HumContratoSerializador(serializers.HyperlinkedModelSerializer):
    contrato_tipo = serializers.PrimaryKeyRelatedField(queryset=HumContratoTipo.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all())
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all())

    class Meta:
        model = HumContrato
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'estado_terminado', 'contrato_tipo', 'grupo', 'contacto']


class HumContratoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumContrato

    def to_representation(self, instance):
        contacto_numero_identificacion = ''
        contacto_nombre_corto = ''
        if instance.contacto:
            contacto_numero_identificacion = instance.contacto.numero_identificacion
            contacto_nombre_corto = instance.contacto.nombre_corto
        return {
            'contrato_id': instance.id,
            'contrato_contacto_numero_identificacion': contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contacto_nombre_corto
        } 
        