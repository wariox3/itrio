from rest_framework import serializers
from django.db import models
from humano.models.liquidacion import HumLiquidacion
from humano.models.contrato import HumContrato


class HumLiquidacionSerializador(serializers.HyperlinkedModelSerializer):
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())
    class Meta:
        model = HumLiquidacion
        fields = ['id', 'fecha', 'fecha_desde', 'fecha_hasta', 'contrato', 'dias', 'cesantia', 'interes', 'prima'
                  ,'vacacion', 'deduccion', 'adicion', 'total', 'estado_aprobado', 'estado_generado', 'comentario']        

class HumLiquidacionListaSerializador(serializers.HyperlinkedModelSerializer):      
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
                  'total',
                  'estado_generado',
                  'estado_aprobado']      
        select_related_fields = ['contrato', 'contrato__contacto']  