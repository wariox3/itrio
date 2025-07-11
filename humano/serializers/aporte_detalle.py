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


class HumAporteDetalleInformeSerializador(serializers.ModelSerializer):
    aporte_contrato__contrato__contacto__numero_identificacion = serializers.CharField(source='aporte_contrato.contrato.contacto.numero_identificacion', read_only=True)
    aporte_contrato__contrato__contacto__nombre_corto = serializers.CharField(source='aporte_contrato.contrato.contacto.nombre_corto', read_only=True)  
    aporte_contrato__contrato__contacto_id = serializers.IntegerField(source='aporte_contrato.contrato.contacto_id', read_only=True)   
    aporte_contrato__contrato__salario = serializers.IntegerField(source='aporte_contrato.contrato.salario', read_only=True)
    class Meta:
        model = HumAporteDetalle   
        fields = ['id', 'aporte_contrato__contrato__contacto__numero_identificacion', 'aporte_contrato__contrato__contacto__nombre_corto', 
                  'aporte_contrato__contrato__contacto_id', 'ingreso', 'retiro', 'variacion_permanente_salario', 'variacion_transitoria_salario',
                  'suspension_temporal_contrato', 'incapacidad_general', 'licencia_maternidad', 'vacaciones', 'licencia_remunerada', 'dias_incapacidad_laboral',
                  'salario_integral', 'aporte_contrato__contrato__salario', 'horas', 'dias_pension', 'dias_salud', 'dias_riesgos', 'dias_caja', 'base_cotizacion_pension', 
                  'base_cotizacion_salud', 'base_cotizacion_riesgos', 'base_cotizacion_caja', 'tarifa_pension', 'tarifa_salud', 'tarifa_riesgos', 'tarifa_caja', 'tarifa_sena',
                  'tarifa_icbf', 'cotizacion_pension', 'cotizacion_solidaridad_solidaridad', 'cotizacion_solidaridad_subsistencia', 'cotizacion_voluntario_pension_afiliado',
                  'cotizacion_voluntario_pension_aportante', 'cotizacion_salud', 'cotizacion_riesgos', 'cotizacion_caja', 'cotizacion_sena', 'cotizacion_icbf', 'cotizacion_total',
                  'fecha_inicio_incapacidad_general', 'fecha_fin_incapacidad_general', 'fecha_inicio_incapacidad_laboral', 'fecha_fin_incapacidad_laboral', 'fecha_inicio_licencia_maternidad',
                  'fecha_fin_licencia_maternidad', 'fecha_inicio_vacaciones', 'fecha_inicio_vacaciones']
        select_related_fields = ['aporte_contrato']            
