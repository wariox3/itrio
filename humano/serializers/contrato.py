from rest_framework import serializers
from general.models.contacto import Contacto
from humano.models.contrato import HumContrato
from humano.models.contrato_tipo import HumContratoTipo
from humano.models.grupo import HumGrupo

class HumContratoSerializador(serializers.HyperlinkedModelSerializer):
    contrato_tipo = serializers.PrimaryKeyRelatedField(queryset=HumContratoTipo.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all())
    contacto = serializers.PrimaryKeyRelatedField(queryset=Contacto.objects.all())

    class Meta:
        model = HumContrato
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'estado_terminado', 'contrato_tipo', 'grupo', 'contacto']

    def to_representation(self, instance):
        contrato_tipo_nombre = ''
        if instance.contrato_tipo:
            contrato_tipo_nombre = instance.contrato_tipo.nombre
        grupo_nombre = ''
        if instance.grupo:
            grupo_nombre = instance.grupo.nombre        
        contacto_numero_identificacion = ''
        contacto_nombre_corto = ''
        if instance.contacto:
            contacto_numero_identificacion = instance.contacto.numero_identificacion
            contacto_nombre_corto = instance.contacto.nombre_corto
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'estado_terminado': instance.estado_terminado,
            'contrato_tipo_id': instance.contrato_tipo_id,
            'contrato_tipo_nombre': contrato_tipo_nombre,
            'grupo_id': instance.grupo_id,
            'grupo_nombre': grupo_nombre,
            'contacto_id': instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto': contacto_nombre_corto
        } 


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
        