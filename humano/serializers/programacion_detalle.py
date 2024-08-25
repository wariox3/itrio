from rest_framework import serializers
from humano.models.programacion import HumProgramacion
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.contrato import HumContrato

class HumProgramacionDetalleSerializador(serializers.HyperlinkedModelSerializer):
    pago_horas = serializers.BooleanField(required=True)
    pago_auxilio_transporte = serializers.BooleanField(required=True)
    pago_incapacidad = serializers.BooleanField(required=True)
    pago_licencia = serializers.BooleanField(required=True)   
    pago_vacacion = serializers.BooleanField(required=True)
    descuento_salud = serializers.BooleanField(required=True)
    descuento_pension = serializers.BooleanField(required=True)
    descuento_fondo_solidaridad = serializers.BooleanField(required=True)
    descuento_retencion_fuente = serializers.BooleanField(required=True)
    descuento_credito = serializers.BooleanField(required=True)
    descuento_embargo = serializers.BooleanField(required=True)
    adicional = serializers.BooleanField(required=True)    
    programacion = serializers.PrimaryKeyRelatedField(queryset=HumProgramacion.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumProgramacionDetalle
        fields = ['id', 'dias', 'dias_transporte', 'dias_novedad', 'salario', 'fecha_desde', 'fecha_hasta', 'diurna', 'nocturna', 'festiva_diurna', 
                  'festiva_nocturna', 'extra_diurna', 'extra_nocturna', 
                  'extra_festiva_diurna', 'extra_festiva_nocturna', 'recargo_nocturno', 'recargo_festivo_diurno', 'recargo_festivo_nocturno',
                  'programacion', 'contrato', 'ingreso', 'retiro',
                  'pago_horas', 'pago_auxilio_transporte', 'pago_incapacidad', 'pago_licencia', 'pago_vacacion', 
                  'descuento_salud', 'descuento_pension', 'descuento_fondo_solidaridad', 'descuento_retencion_fuente', 
                  'descuento_credito', 'descuento_embargo', 'adicional', 'devengado', 'deduccion', 'total']

    def to_representation(self, instance):      
        if instance.contrato:
            if instance.contrato.contacto:
                contrato_contacto_numero_identificacion = instance.contrato.contacto.numero_identificacion
                contrato_contacto_nombre_corto = instance.contrato.contacto.nombre_corto
        return {
            'id': instance.id,
            'programacion_id': instance.programacion_id,
            'dias': instance.dias,
            'dias_transporte': instance.dias_transporte,
            'salario': instance.salario,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'total': instance.total,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'diurna': instance.diurna ,
            'nocturna': instance.nocturna ,
            'festiva_diurna': instance.festiva_diurna ,
            'festiva_nocturna': instance.festiva_nocturna ,
            'extra_diurna': instance.extra_diurna ,
            'extra_nocturna': instance.extra_nocturna ,
            'extra_festiva_diurna': instance.extra_festiva_diurna ,
            'extra_festiva_nocturna': instance.extra_festiva_nocturna ,
            'recargo_nocturno': instance.recargo_nocturno ,
            'recargo_festivo_diurno': instance.recargo_festivo_diurno ,
            'recargo_festivo_nocturno': instance.recargo_festivo_nocturno ,
            'contrato_id': instance.contrato_id,
            'contrato_contacto_id': instance.contrato.contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto,
            'ingreso': instance.ingreso,
            'retiro': instance.retiro,
            'pago_horas': instance.pago_horas,
            'pago_auxilio_transporte' : instance.pago_auxilio_transporte,
            'pago_incapacidad' : instance.pago_incapacidad,
            'pago_licencia' : instance.pago_licencia,
            'pago_vacacion' : instance.pago_vacacion,
            'descuento_salud' : instance.descuento_salud,
            'descuento_pension' : instance.descuento_pension,
            'descuento_fondo_solidaridad': instance.descuento_fondo_solidaridad,
            'descuento_retencion_fuente' : instance.descuento_retencion_fuente,                        
            'descuento_credito': instance.descuento_credito,
            'descuento_embargo' : instance.descuento_embargo,
            'adicional': instance.adicional
        }         
        