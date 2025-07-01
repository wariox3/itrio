from rest_framework import serializers
from humano.models.aporte_contrato import HumAporteContrato
from humano.models.aporte import HumAporte
from humano.models.contrato import HumContrato
from humano.models.entidad import HumEntidad
from humano.models.riesgo import HumRiesgo
from general.models.ciudad import GenCiudad


class HumAporteContratoSerializador(serializers.ModelSerializer):
    contrato__contacto__numero_identificacion = serializers.CharField(source='contrato.contacto.numero_identificacion', read_only=True)
    contrato__contacto__nombre_corto = serializers.CharField(source='contrato.contacto.nombre_corto', read_only=True)  
    contrato__contacto_id = serializers.IntegerField(source='contrato.contacto_id', read_only=True)  

    class Meta:
        model = HumAporteContrato
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'dias', 'salario',
                  'base_cotizacion',
                  'aporte', 'contrato', 'ingreso', 'retiro', 'error_terminacion',
                  'ciudad_labora', 'entidad_salud', 'entidad_pension', 'entidad_caja', 'entidad_riesgo', 
                  'entidad_sena', 'entidad_icbf', 'riesgo', 'cotizacion_pension', 'cotizacion_voluntario_pension_afiliado',
                  'cotizacion_voluntario_pension_aportante', 'cotizacion_solidaridad_solidaridad', 'cotizacion_solidaridad_subsistencia',
                  'cotizacion_pension_total',
                  'cotizacion_salud', 'cotizacion_riesgos', 'cotizacion_caja', 'cotizacion_sena', 'cotizacion_icbf', 'cotizacion_total',
                  'cotizacion_pension_empresa', 'cotizacion_pension_empleado', 'cotizacion_salud_empresa', 'cotizacion_salud_empleado', 'contrato__contacto__numero_identificacion',
                  'contrato__contacto__nombre_corto', 'contrato__contacto_id']           
        select_related_fields = ['contrato']

#deprecated
class HumAporteContrato1Serializador(serializers.HyperlinkedModelSerializer):
    aporte = serializers.PrimaryKeyRelatedField(queryset=HumAporte.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    ciudad_labora = serializers.PrimaryKeyRelatedField(queryset=GenCiudad.objects.all())
    entidad_salud = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())
    entidad_pension = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())
    entidad_caja = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())
    entidad_riesgo = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())
    entidad_sena = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())
    entidad_icbf = serializers.PrimaryKeyRelatedField(queryset=HumEntidad.objects.all())
    riesgo = serializers.PrimaryKeyRelatedField(queryset=HumRiesgo.objects.all())

    class Meta:
        model = HumAporteContrato
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'dias', 'salario',
                  'base_cotizacion',
                  'aporte', 'contrato', 'ingreso', 'retiro', 'error_terminacion',
                  'ciudad_labora', 'entidad_salud', 'entidad_pension', 'entidad_caja', 'entidad_riesgo', 
                  'entidad_sena', 'entidad_icbf', 'riesgo', 'cotizacion_pension', 'cotizacion_voluntario_pension_afiliado',
                  'cotizacion_voluntario_pension_aportante', 'cotizacion_solidaridad_solidaridad', 'cotizacion_solidaridad_subsistencia',
                  'cotizacion_pension_total',
                  'cotizacion_salud', 'cotizacion_riesgos', 'cotizacion_caja', 'cotizacion_sena', 'cotizacion_icbf', 'cotizacion_total',
                  'cotizacion_pension_empresa', 'cotizacion_pension_empleado', 'cotizacion_salud_empresa', 'cotizacion_salud_empleado']        

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
            'fecha_desde': instance.fecha_desde,
            'fecha_hasta': instance.fecha_hasta,
            'dias': instance.dias,
            'salario': instance.salario,
            'base_cotizacion': instance.base_cotizacion,
            'aporte_id': instance.aporte_id,
            'cotrato_id': instance.contrato_id,
            'contrato_contacto_id': contrato_contacto_id,
            'contrato_contacto_numero_identificacion': contrato_contacto_numero_identificacion,
            'contrato_contacto_nombre_corto': contrato_contacto_nombre_corto,
            'ingreso': instance.ingreso,
            'retiro': instance.retiro,
            'error_terminacion': instance.error_terminacion
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