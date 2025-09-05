from rest_framework import serializers
from django.db import models
from humano.models.liquidacion import HumLiquidacion
from humano.models.contrato import HumContrato


class HumLiquidacionSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    class Meta:
        model = HumLiquidacion
        fields = ['id', 'fecha', 'fecha_desde', 'fecha_hasta', 'contrato', 'dias', 'cesantia', 'interes', 'prima'
                  ,'vacacion', 'deduccion', 'adicion', 'total', 'salario', 'estado_aprobado', 'estado_generado', 'comentario',
                  'fecha_ultimo_pago', 'fecha_ultimo_pago_prima', 'fecha_ultimo_pago_cesantia', 'fecha_ultimo_pago_vacacion']        

class HumLiquidacionListaSerializador(serializers.HyperlinkedModelSerializer):      
    contrato__contacto__numero_identificacion = serializers.CharField(source='contrato.contacto.numero_identificacion', read_only=True)
    contrato__contacto__nombre_corto = serializers.CharField(source='contrato.contacto.nombre_corto', read_only=True)   
    contrato__salario = serializers.IntegerField(source='contrato.salario', read_only=True)   
    
    class Meta:
        model = HumLiquidacion
        fields = ['id', 
                  'fecha',    
                  'contrato__contacto__numero_identificacion',      
                  'contrato__contacto__nombre_corto', 
                  'contrato_id',                       
                  'fecha_desde',
                  'fecha_hasta',
                  'total',
                  'dias',
                  'cesantia',
                  'interes',
                  'prima',
                  'vacacion',
                  'deduccion',
                  'adicion',
                  'estado_generado',
                  'estado_aprobado',
                  'comentario']      
        select_related_fields = ['contrato', 'contrato__contacto']  

class HumLiquidacionDetalleSerializador(serializers.HyperlinkedModelSerializer):      
    contrato__contacto__numero_identificacion = serializers.CharField(source='contrato.contacto.numero_identificacion', read_only=True)
    contrato__contacto__nombre_corto = serializers.CharField(source='contrato.contacto.nombre_corto', read_only=True)   
    
    class Meta:
        model = HumLiquidacion
        fields = ['id', 
                  'fecha',    
                  'contrato__contacto__numero_identificacion',      
                  'contrato__contacto__nombre_corto', 
                  'contrato_id',                       
                  'fecha_desde',
                  'fecha_hasta',
                  'dias',
                  'dias_cesantia',
                  'dias_prima',
                  'dias_vacacion',
                  'cesantia',
                  'interes',
                  'prima',
                  'vacacion',
                  'deduccion',
                  'adicion',
                  'total',
                  'fecha_ultimo_pago',
                  'fecha_ultimo_pago_prima',
                  'fecha_ultimo_pago_cesantia',
                  'fecha_ultimo_pago_vacacion',
                  'estado_generado',
                  'estado_aprobado',
                  'comentario']      
        select_related_fields = ['contrato', 'contrato__contacto']         