from rest_framework import serializers
from humano.models.programacion import HumProgramacion
from humano.models.grupo import HumGrupo
from humano.models.pago_tipo import HumPagoTipo
from humano.models.periodo import HumPeriodo

class HumProgramacionSerializador(serializers.HyperlinkedModelSerializer):
    fecha_hasta_periodo = serializers.DateField(required=False)
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
    pago_tipo = serializers.PrimaryKeyRelatedField(queryset=HumPagoTipo.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all())
    periodo = serializers.PrimaryKeyRelatedField(queryset=HumPeriodo.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumProgramacion
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'nombre', 'grupo', 'pago_tipo', 
                  'devengado', 'deduccion', 'total', 'contratos', 'dias', 'comentario',
                  'pago_horas', 'pago_auxilio_transporte', 'pago_incapacidad', 'pago_licencia', 'pago_vacacion', 
                  'pago_cesantia', 'pago_interes', 'pago_prima',
                  'descuento_salud', 'descuento_pension', 'descuento_fondo_solidaridad', 'descuento_retencion_fuente', 
                  'descuento_credito', 'descuento_embargo', 'adicional', 'periodo']

    def to_representation(self, instance):      
        pago_tipo_nombre = ''
        if instance.pago_tipo:
            pago_tipo_nombre = instance.pago_tipo.nombre
        grupo_nombre = ''            
        if instance.grupo:
            grupo_nombre = instance.grupo.nombre
        periodo_nombre = ''
        if instance.periodo:
            periodo_nombre = instance.periodo.nombre
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'fecha_hasta_periodo': instance.fecha_hasta_periodo,
            'nombre': instance.nombre,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'total': instance.total,
            'contratos': instance.contratos,
            'dias': instance.dias,
            'comentario': instance.comentario,
            'pago_horas': instance.pago_horas,
            'pago_auxilio_transporte': instance.pago_auxilio_transporte,
            'pago_incapacidad': instance.pago_incapacidad,
            'pago_licencia': instance.pago_licencia,
            'pago_vacacion': instance.pago_vacacion,
            'pago_cesantia': instance.pago_cesantia,
            'pago_interes': instance.pago_interes,
            'pago_prima': instance.pago_prima,
            'descuento_salud': instance.descuento_salud,
            'descuento_pension': instance.descuento_pension,
            'descuento_fondo_solidaridad': instance.descuento_fondo_solidaridad,
            'descuento_retencion_fuente': instance.descuento_retencion_fuente,            
            'adicional': instance.adicional,
            'descuento_credito': instance.descuento_credito,
            'descuento_embargo': instance.descuento_embargo,
            'pago_tipo_id': instance.pago_tipo_id,
            'pago_tipo_nombre': pago_tipo_nombre,
            'grupo_id': instance.grupo_id,
            'grupo_nombre': grupo_nombre,
            'periodo_id': instance.periodo_id,
            'periodo_nombre': periodo_nombre,
            'estado_generado': instance.estado_generado,
            'estado_aprobado': instance.estado_aprobado
        }        
    
class HumProgramacionExcelSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumProgramacion

    def to_representation(self, instance):      
        pago_tipo_nombre = ''
        if instance.pago_tipo:
            pago_tipo_nombre = instance.pago_tipo.nombre
        grupo_nombre = ''            
        if instance.grupo:
            grupo_nombre = instance.grupo.nombre
        periodo_nombre = ''
        if instance.periodo:
            periodo_nombre = instance.periodo.nombre
        return {
            'id': instance.id,
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'fecha_hasta_periodo': instance.fecha_hasta_periodo,
            'nombre': instance.nombre,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'total': instance.total,
            'contratos': instance.contratos,
            'dias': instance.dias,
            'comentario': instance.comentario,
            'pago_horas': instance.pago_horas,
            'pago_auxilio_transporte': instance.pago_auxilio_transporte,
            'pago_incapacidad': instance.pago_incapacidad,
            'pago_licencia': instance.pago_licencia,
            'pago_vacacion': instance.pago_vacacion,
            'pago_cesantia': instance.pago_cesantia,
            'pago_interes': instance.pago_interes,
            'pago_prima': instance.pago_prima,
            'descuento_salud': instance.descuento_salud,
            'descuento_pension': instance.descuento_pension,
            'descuento_fondo_solidaridad': instance.descuento_fondo_solidaridad,
            'descuento_retencion_fuente': instance.descuento_retencion_fuente,            
            'adicional': instance.adicional,
            'descuento_credito': instance.descuento_credito,
            'descuento_embargo': instance.descuento_embargo,
            'pago_tipo_id': instance.pago_tipo_id,
            'pago_tipo_nombre': pago_tipo_nombre,
            'grupo_id': instance.grupo_id,
            'grupo_nombre': grupo_nombre,
            'periodo_id': instance.periodo_id,
            'periodo_nombre': periodo_nombre,
            'estado_generado': instance.estado_generado,
            'estado_aprobado': instance.estado_aprobado
        }        
    