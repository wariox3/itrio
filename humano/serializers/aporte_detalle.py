from rest_framework import serializers
from humano.models.aporte_detalle import HumAporteDetalle

class HumAporteDetalleSerializador(serializers.ModelSerializer):   
    aporte_contrato__contrato__contacto__numero_identificacion = serializers.CharField(source='aporte_contrato.contrato.contacto.numero_identificacion', read_only=True)
    aporte_contrato__contrato__contacto__nombre_corto = serializers.CharField(source='aporte_contrato.contrato.contacto.nombre_corto', read_only=True)  
    aporte_contrato__contrato__contacto_id = serializers.IntegerField(source='aporte_contrato.contrato.contacto_id', read_only=True)   
    
    class Meta:
        model = HumAporteDetalle
        fields = ['id','ingreso', 'retiro', 'aporte_contrato', 'salario_integral', 'variacion_permanente_salario', 
                  'variacion_transitoria_salario', 'suspension_temporal_contrato', 'incapacidad_general',
                  'licencia_maternidad', 'vacaciones', 'licencia_remunerada', 'aporte_voluntario_pension',
                  'variacion_centro_trabajo', 'dias_incapacidad_laboral',                  
                  'horas', 'dias_pension',  'dias_salud', 'dias_riesgos', 'dias_caja', 
                  'fecha_ingreso', 'fecha_retiro',
                  'fecha_inicio_incapacidad_general', 'fecha_fin_incapacidad_general',
                  'fecha_inicio_licencia_maternidad', 'fecha_fin_licencia_maternidad',
                  'fecha_inicio_suspension_temporal_contrato', 'fecha_fin_suspension_temporal_contrato', 
                  'fecha_inicio_vacaciones', 'fecha_fin_vacaciones',
                  'fecha_inicio_incapacidad_laboral', 'fecha_fin_incapacidad_laboral',
                  'base_cotizacion_pension', 'base_cotizacion_salud', 'base_cotizacion_riesgos', 'base_cotizacion_caja',
                  'tarifa_pension', 'tarifa_salud', 'tarifa_riesgos', 'tarifa_caja', 'tarifa_sena', 'tarifa_icbf', 
                  'cotizacion_pension', 'cotizacion_solidaridad_solidaridad', 'cotizacion_solidaridad_subsistencia', 
                  'cotizacion_voluntario_pension_afiliado', 'cotizacion_voluntario_pension_aportante', 'cotizacion_salud', 
                  'cotizacion_riesgos', 'cotizacion_caja', 'cotizacion_sena', 'cotizacion_icbf', 'cotizacion_total',
                  'aporte_contrato__contrato__contacto__numero_identificacion', 'aporte_contrato__contrato__contacto__nombre_corto',
                  'aporte_contrato__contrato__contacto_id']
        select_related_fields = ['aporte_contrato']


    # def to_representation(self, instance):         
    #     aporte_contrato_contrato_contacto_numero_identificacion = ""
    #     aporte_contrato_contrato_contacto_nombre_corto = ""
    #     aporte_contrato_contrato_id = ""
    #     aporte_contrato_salario = ""
    #     if instance.aporte_contrato:
    #         aporte_contrato_contrato_id = instance.aporte_contrato.contrato_id
    #         aporte_contrato_salario = instance.aporte_contrato.salario
    #         if instance.aporte_contrato.contrato:
    #             if instance.aporte_contrato.contrato.contacto:
    #                 aporte_contrato_contrato_contacto_numero_identificacion = instance.aporte_contrato.contrato.contacto.numero_identificacion
    #                 aporte_contrato_contrato_contacto_nombre_corto = instance.aporte_contrato.contrato.contacto.nombre_corto
        
    #     return {
    #         'id': instance.id,
    #         'aporte_contrato_contrato_contacto_numero_identificacion': aporte_contrato_contrato_contacto_numero_identificacion,
    #         'aporte_contrato_contrato_contacto_nombre_corto': aporte_contrato_contrato_contacto_nombre_corto,
    #         'aport_contrato_contrato_id': aporte_contrato_contrato_id,            
    #         'ingreso': instance.ingreso,
    #         'retiro': instance.retiro,
    #         'variacion_permanente_salario': instance.variacion_permanente_salario,
    #         'variacion_transitoria_salario': instance.variacion_transitoria_salario,
    #         'suspension_temporal_contrato': instance.suspension_temporal_contrato,
    #         'incapacidad_general': instance.incapacidad_general,
    #         'licencia_maternidad': instance.licencia_maternidad,
    #         'vacaciones': instance.vacaciones,
    #         'licencia_remunerada': instance.licencia_remunerada,
    #         'dias_incapacidad_laboral': instance.dias_incapacidad_laboral,
    #         'salario_integral': instance.salario_integral,
    #         'aporte_contrato_salario': aporte_contrato_salario,
    #         'horas': instance.horas,
    #         'dias_pension': instance.dias_pension,
    #         'dias_salud': instance.dias_salud,
    #         'dias_riesgos': instance.dias_riesgos,
    #         'dias_caja': instance.dias_caja,
    #         'base_cotizacion_pension': instance.base_cotizacion_pension,
    #         'base_cotizacion_salud': instance.base_cotizacion_salud,
    #         'base_cotizacion_riesgos': instance.base_cotizacion_riesgos,
    #         'base_cotizacion_caja': instance.base_cotizacion_caja,
    #         'tarifa_pension': instance.tarifa_pension,
    #         'tarifa_salud': instance.tarifa_salud,
    #         'tarifa_riesgos': instance.tarifa_riesgos,
    #         'tarifa_caja': instance.tarifa_caja,
    #         'tarifa_sena': instance.tarifa_sena,
    #         'tarifa_icbf': instance.tarifa_icbf,
    #         'cotizacion_pension': instance.cotizacion_pension,
    #         'cotizacion_solidaridad_solidaridad': instance.cotizacion_solidaridad_solidaridad,
    #         'cotizacion_solidaridad_subsistencia': instance.cotizacion_solidaridad_subsistencia,
    #         'cotizacion_voluntario_pension_afiliado': instance.cotizacion_voluntario_pension_afiliado,
    #         'cotizacion_voluntario_pension_aportante': instance.cotizacion_voluntario_pension_aportante,
    #         'cotizacion_salud': instance.cotizacion_salud,
    #         'cotizacion_riesgos': instance.cotizacion_riesgos,
    #         'cotizacion_caja': instance.cotizacion_caja,
    #         'cotizacion_sena': instance.cotizacion_sena,
    #         'cotizacion_icbf': instance.cotizacion_icbf,
    #         'cotizacion_total': instance.cotizacion_total
    #     } 

class HumAporteDetalleExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HumAporteDetalle   

    def to_representation(self, instance):         
        aporte_contrato_contrato_contacto_numero_identificacion = ""
        aporte_contrato_contrato_contacto_nombre_corto = ""
        aporte_contrato_contrato_id = ""
        aporte_contrato_salario = ""
        if instance.aporte_contrato:
            aporte_contrato_contrato_id = instance.aporte_contrato.contrato_id
            aporte_contrato_salario = instance.aporte_contrato.salario
            if instance.aporte_contrato.contrato:
                if instance.aporte_contrato.contrato.contacto:
                    aporte_contrato_contrato_contacto_numero_identificacion = instance.aporte_contrato.contrato.contacto.numero_identificacion
                    aporte_contrato_contrato_contacto_nombre_corto = instance.aporte_contrato.contrato.contacto.nombre_corto
        
        return {
            'ID': instance.id,
            'IDENTIFICACION': aporte_contrato_contrato_contacto_numero_identificacion,
            'EMPLEADO': aporte_contrato_contrato_contacto_nombre_corto,
            'CONTRATO': aporte_contrato_contrato_id,            
            'ING': instance.ingreso,
            'RET': instance.retiro,
            'VSP': instance.variacion_permanente_salario,
            'VST': instance.variacion_transitoria_salario,
            'SLN': instance.suspension_temporal_contrato,
            'IGE': instance.incapacidad_general,
            'LM': instance.licencia_maternidad,
            'VAC': instance.vacaciones,
            'LRM': instance.licencia_remunerada,
            'D_IRP': instance.dias_incapacidad_laboral,
            'SI': instance.salario_integral,
            'SALARIO': aporte_contrato_salario,
            'H': instance.horas,
            'D_P': instance.dias_pension,
            'D_S': instance.dias_salud,
            'D_R': instance.dias_riesgos,
            'D_C': instance.dias_caja,
            'BC_P': instance.base_cotizacion_pension,
            'BC_S': instance.base_cotizacion_salud,
            'BC_R': instance.base_cotizacion_riesgos,
            'BC_C': instance.base_cotizacion_caja,
            'T_P': instance.tarifa_pension,
            'T_S': instance.tarifa_salud,
            'T_R': instance.tarifa_riesgos,
            'T_C': instance.tarifa_caja,
            'T_S': instance.tarifa_sena,
            'T_ICBF': instance.tarifa_icbf,
            'C_P': instance.cotizacion_pension,
            'F_SOL': instance.cotizacion_solidaridad_solidaridad,
            'F_SUB': instance.cotizacion_solidaridad_subsistencia,
            'VOL_AFI': instance.cotizacion_voluntario_pension_afiliado,
            'VOL_APO': instance.cotizacion_voluntario_pension_aportante,
            'C_S': instance.cotizacion_salud,
            'C_R': instance.cotizacion_riesgos,
            'C_C': instance.cotizacion_caja,
            'C_SENA': instance.cotizacion_sena,
            'C_ICBF': instance.cotizacion_icbf,
            'TOTAL': instance.cotizacion_total,
            'FECHA_INICIO_INC_GEN': instance.fecha_inicio_incapacidad_general,
            'FECHA_FIN_INC_GEN': instance.fecha_fin_incapacidad_general,
            'FECHA_INICIO_LAB_GEN': instance.fecha_inicio_incapacidad_laboral,
            'FECHA_FIN_LAB_GEN': instance.fecha_fin_incapacidad_laboral,
            'FECHA_INICIO_LIC_MAT': instance.fecha_inicio_licencia_maternidad,
            'FECHA_FIN_LIC_MAT': instance.fecha_fin_licencia_maternidad,
            'FECHA_INICIO_VAC': instance.fecha_inicio_vacaciones,
            'FECHA_FIN_VAC': instance.fecha_inicio_vacaciones

        }                