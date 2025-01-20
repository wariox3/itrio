from rest_framework import serializers
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from humano.models.contrato import HumContrato
from humano.models.contrato_tipo import HumContratoTipo
from humano.models.grupo import HumGrupo
from humano.models.sucursal import HumSucursal
from humano.models.riesgo import HumRiesgo
from humano.models.tipo_cotizante import HumTipoCotizante
from humano.models.subtipo_cotizante import HumSubtipoCotizante
from humano.models.cargo import HumCargo
from humano.models.salud import HumSalud
from humano.models.pension import HumPension
from humano.models.entidad import HumEntidad

class HumContratoSerializador(serializers.HyperlinkedModelSerializer):
    contrato_tipo = serializers.PrimaryKeyRelatedField(queryset=HumContratoTipo.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all())
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all())
    ciudad_contrato = serializers.PrimaryKeyRelatedField(queryset=GenCiudad.objects.all())
    ciudad_labora = serializers.PrimaryKeyRelatedField(queryset=GenCiudad.objects.all())
    sucursal = serializers.PrimaryKeyRelatedField(queryset=HumSucursal.objects.all(), default=None, allow_null=True)
    riesgo = serializers.PrimaryKeyRelatedField(queryset=HumRiesgo.objects.all())
    cargo = serializers.PrimaryKeyRelatedField(queryset=HumCargo.objects.all())
    salud = serializers.PrimaryKeyRelatedField(queryset=HumSalud.objects.all())
    pension = serializers.PrimaryKeyRelatedField(queryset=HumPension.objects.all())
    tipo_cotizante = serializers.PrimaryKeyRelatedField(queryset=HumTipoCotizante.objects.all())
    subtipo_cotizante = serializers.PrimaryKeyRelatedField(queryset=HumSubtipoCotizante.objects.all())
    entidad_salud = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)
    entidad_pension = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)    
    entidad_caja = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)
    entidad_cesantias = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumContrato
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'salario', 'auxilio_transporte', 'salario_integral', 'estado_terminado', 
                  'comentario', 'contrato_tipo', 'grupo', 'contacto', 'sucursal', 'riesgo', 'cargo', 'tipo_cotizante', 'subtipo_cotizante',
                  'salud', 'pension', 'ciudad_contrato', 'ciudad_labora', 'entidad_salud', 'entidad_pension', 'entidad_caja', 'entidad_cesantias']

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
        sucursal_nombre = ''
        if instance.sucursal:
            sucursal_nombre = instance.sucursal.nombre
        riesgo_nombre = ''
        if instance.riesgo:
            riesgo_nombre = instance.riesgo.nombre
        cargo_nombre = ''
        if instance.cargo:
            cargo_nombre = instance.cargo.nombre
        tipo_cotizante_nombre = ''
        if instance.tipo_cotizante:
            tipo_cotizante_nombre = instance.tipo_cotizante.nombre
        subtipo_cotizante_nombre = ''
        if instance.subtipo_cotizante:
            subtipo_cotizante_nombre = instance.subtipo_cotizante.nombre
        salud_nombre = ''
        if instance.salud:
            salud_nombre = instance.salud.nombre
        pension_nombre = ''
        if instance.pension:
            pension_nombre = instance.pension.nombre
        ciudad_contrato_nombre = ''
        if instance.ciudad_contrato:            
            ciudad_contrato_nombre = instance.ciudad_contrato.nombre
        ciudad_labora_nombre = ''
        if instance.ciudad_labora:            
            ciudad_labora_nombre = instance.ciudad_labora.nombre  
        entidad_salud_nombre = ''
        if instance.entidad_salud:
            entidad_salud_nombre = instance.entidad_salud.nombre
        entidad_pension_nombre = ''
        if instance.entidad_pension:
            entidad_pension_nombre = instance.entidad_pension.nombre
        entidad_cesantias_nombre = ''
        if instance.entidad_cesantias:
            entidad_cesantias_nombre = instance.entidad_cesantias.nombre        
        entidad_caja_nombre = ''
        if instance.entidad_caja:
            entidad_caja_nombre = instance.entidad_caja.nombre
        fecha_hasta = instance.fecha_hasta
        if instance.estado_terminado == False:
            if instance.contrato_tipo_id == 1:
                fecha_hasta = None
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': fecha_hasta,
            'salario': instance.salario,
            'auxilio_transporte': instance.auxilio_transporte,
            'salario_integral': instance.salario_integral,
            'estado_terminado': instance.estado_terminado,
            'comentario': instance.comentario,
            'contrato_tipo_id': instance.contrato_tipo_id,
            'contrato_tipo_nombre': contrato_tipo_nombre,
            'grupo_id': instance.grupo_id,
            'grupo_nombre': grupo_nombre,
            'contacto_id': instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto': contacto_nombre_corto,
            'sucursal_id': instance.sucursal_id,
            'sucursal_nombre': sucursal_nombre,
            'riesgo_id': instance.riesgo_id,
            'riesgo_nombre': riesgo_nombre,
            'cargo_id': instance.cargo_id,
            'cargo_nombre': cargo_nombre,
            'tipo_cotizante_id': instance.tipo_cotizante_id,
            'tipo_cotizante_nombre': tipo_cotizante_nombre,
            'subtipo_cotizante_id': instance.subtipo_cotizante_id,
            'subtipo_cotizante_nombre': subtipo_cotizante_nombre,
            'salud_id': instance.salud_id,
            'salud_nombre': salud_nombre,
            'pension_id': instance.pension_id,
            'pension_nombre': pension_nombre,
            'ciudad_contrato_id': instance.ciudad_contrato_id,
            'ciudad_contrato_nombre': ciudad_contrato_nombre,
            'ciudad_labora_id': instance.ciudad_labora_id,
            'ciudad_labora_nombre': ciudad_labora_nombre,
            'entidad_salud_id': instance.entidad_salud_id,
            'entidad_salud_nombre': entidad_salud_nombre,
            'entidad_pension_id': instance.entidad_pension_id,
            'entidad_pension_nombre': entidad_pension_nombre,
            'entidad_cesantias_id': instance.entidad_cesantias_id,
            'entidad_cesantias_nombre': entidad_cesantias_nombre,
            'entidad_caja_id': instance.entidad_caja_id,
            'entidad_caja_nombre': entidad_caja_nombre
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
        