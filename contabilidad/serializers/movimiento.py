from rest_framework import serializers
from contabilidad.models.movimiento import ConMovimiento
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.periodo import ConPeriodo
from contabilidad.models.comprobante import ConComprobante
from contabilidad.models.grupo import ConGrupo
from general.models.contacto import GenContacto
from general.models.documento import GenDocumento

class ConMovimientoSerializador(serializers.HyperlinkedModelSerializer):    
    comprobante = serializers.PrimaryKeyRelatedField(queryset=ConComprobante.objects.all())
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all())
    periodo = serializers.PrimaryKeyRelatedField(queryset=ConPeriodo.objects.all())
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), allow_null=True, default=None)
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), allow_null=True)        
    grupo = serializers.PrimaryKeyRelatedField(queryset=ConGrupo.objects.all(), allow_null=True, default=None)
    detalle = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    
    class Meta:
        model = ConMovimiento
        fields = ['id', 'numero', 'fecha', 'debito', 'credito', 'base', 'naturaleza', 'cuenta', 'comprobante', 'contacto', 'documento', 
                  'periodo', 'grupo', 'detalle', 'cierre']

    def validate(self, data):
        cuenta = data.get('cuenta')
        base = data.get('base', 0)
        if cuenta:
            if cuenta.permite_movimiento is False:
                raise serializers.ValidationError({"cuenta": "La cuenta no permite movimientos."})
            if cuenta.exige_grupo and data.get('grupo') is None:
                raise serializers.ValidationError({"grupo": "La cuenta exige grupo."})
            if cuenta.exige_base and base == 0:
                raise serializers.ValidationError({"base": "Si la cuenta exige base, la base no puede ser 0."})
            if cuenta.exige_contacto and data.get('contacto') is None:
                raise serializers.ValidationError({"contacto": "La cuenta exige contacto."})
        return data

    def to_representation(self, instance):
        cuenta_codigo = ''
        cuenta_nombre = ''
        if instance.cuenta:
            cuenta_codigo = instance.cuenta.codigo
            cuenta_nombre = instance.cuenta.nombre
        comprobante_codigo = ''
        comprobante_nombre = ''
        if instance.comprobante:
            comprobante_codigo = instance.comprobante.codigo
            comprobante_nombre = instance.comprobante.nombre
        grupo_codigo = ''
        grupo_nombre = ''
        if instance.grupo:
            grupo_codigo = instance.grupo.codigo
            grupo_nombre = instance.grupo.nombre
        contacto_nombre_corto = ''
        contacto_numero_identificacion = ''
        if instance.contacto:
            contacto_numero_identificacion = instance.contacto.numero_identificacion
            contacto_nombre_corto = instance.contacto.nombre_corto

        return {
            'id': instance.id,
            'numero': instance.numero,
            'fecha': instance.fecha,
            'debito': instance.debito ,
            'credito': instance.credito ,
            'base': instance.base ,
            'naturaleza': instance.naturaleza,
            'detalle': instance.detalle,
            'cierre': instance.cierre,
            'cuenta_id': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,
            'cuenta_nombre': cuenta_nombre,
            'comprobante_id': instance.comprobante_id,
            'comprobante_codigo': comprobante_codigo,
            'comprobante_nombre': comprobante_nombre,
            'grupo_id': instance.grupo_id,
            'grupo_codigo': grupo_codigo,
            'grupo_nombre': grupo_nombre,
            'contacto_id': instance.contacto_id,
            'contacto_numero_identificacion': contacto_numero_identificacion,
            'contacto_nombre_corto': contacto_nombre_corto,
            'documento_id': instance.documento_id,
            'periodo_id': instance.periodo_id
        } 

class ConMovimientoExcelSerializador(serializers.HyperlinkedModelSerializer):    

    class Meta:
        model = ConMovimiento

    def to_representation(self, instance):
        cuenta_codigo = ''
        cuenta_nombre = ''
        if instance.cuenta:
            cuenta_codigo = instance.cuenta.codigo
            cuenta_nombre = instance.cuenta.nombre
        comprobante_codigo = ''
        comprobante_nombre = ''
        if instance.comprobante:
            comprobante_codigo = instance.comprobante.codigo
            comprobante_nombre = instance.comprobante.nombre
        grupo_codigo = ''
        grupo_nombre = ''
        if instance.grupo:
            grupo_codigo = instance.grupo.codigo
            grupo_nombre = instance.grupo.nombre
        contacto_nombre_corto = ''
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
        return {
            'ID': instance.id,
            'COMPROBANTE': comprobante_codigo,
            'COMPROBANTE_NOMBRE': comprobante_nombre,
            'NUMERO': instance.numero,
            'FECHA': instance.fecha,
            'CUENTA': cuenta_codigo,
            'CUENTA_NOMBRE': cuenta_nombre,
            'DEBITO': instance.debito ,
            'CREDITO': instance.credito ,
            'BASE': instance.base ,
            'NAT': instance.naturaleza ,                                            
            'GRUPO': grupo_codigo,
            'GRUPO_NOMBRE': grupo_nombre,
            'IDENTIFICACION': instance.contacto_id,
            'NOMBRE_CORTO': contacto_nombre_corto,
            'DOCUMENTO_ID': instance.documento_id,
            'PERIODO': instance.periodo_id
        }             
        