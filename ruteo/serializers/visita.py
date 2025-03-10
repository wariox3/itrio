from rest_framework import serializers
from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from general.models.ciudad import GenCiudad

class RutVisitaSerializador(serializers.HyperlinkedModelSerializer):    
    destinatario_correo = serializers.CharField(allow_null=True)
    documento = serializers.CharField(allow_null=True)
    despacho = serializers.PrimaryKeyRelatedField(queryset=RutDespacho.objects.all(), default=None, allow_null=True)    
    ciudad = serializers.PrimaryKeyRelatedField(queryset=GenCiudad.objects.all(), default=None, allow_null=True)
    
    class Meta:
        model = RutVisita
        fields = ['id', 'guia', 'numero', 'fecha', 'documento', 'destinatario', 'destinatario_direccion', 'destinatario_direccion_formato', 
                  'destinatario_telefono', 'destinatario_correo', 'peso', 'volumen', 'tiempo_servicio', 'latitud', 'longitud', 'estado_decodificado', 
                  'estado_decodificado_alerta', 'orden', 'distancia_proxima',
                  'ciudad', 'despacho', 'franja_id', 'franja_codigo', 'resultados', 'estado_entregado']

    def to_representation(self, instance): 
        ciudad_nombre = ''
        if instance.ciudad:
            ciudad_nombre = instance.ciudad.nombre       
        return {
            'id': instance.id,  
            'guia': instance.guia,
            'numero': instance.numero,
            'fecha': instance.fecha,
            'documento': instance.documento,
            'destinatario': instance.destinatario,
            'destinatario_direccion': instance.destinatario_direccion,
            'destinatario_direccion_formato': instance.destinatario_direccion_formato,
            'ciudad_id': instance.ciudad_id,
            'ciudad_nombre':ciudad_nombre,
            'destinatario_telefono': instance.destinatario_telefono,
            'destinatario_correo': instance.destinatario_correo,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'tiempo_servicio': instance.tiempo_servicio,
            'estado_decodificado': instance.estado_decodificado,
            'estado_decodificado_alerta': instance.estado_decodificado_alerta,
            'estado_despacho': instance.estado_despacho,
            'estado_entregado': instance.estado_entregado,
            'latitud': instance.latitud,
            'longitud': instance.longitud,
            'orden': instance.orden,
            'distancia_proxima': instance.distancia_proxima,
            'franja_id': instance.franja_id,
            'franja_codigo': instance.franja_codigo,
            'despacho_id': instance.despacho_id,
            'resultados': instance.resultados
        }

class RutVisitaExcelSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutVisita

    def to_representation(self, instance): 
        ciudad_nombre = ''
        if instance.ciudad:
            ciudad_nombre = instance.ciudad.nombre     
        return {
            'id': instance.id,  
            'guia': instance.guia,
            'numero': instance.guia,
            'fecha': instance.fecha,
            'documento': instance.documento,
            'destinatario': instance.destinatario,
            'destinatario_direccion': instance.destinatario_direccion,
            'destinatario_direccion_formato': instance.destinatario_direccion_formato,
            'ciudad_id': instance.ciudad_id,
            'ciudad_nombre':ciudad_nombre,
            'destinatario_telefono': instance.destinatario_telefono,
            'destinatario_correo': instance.destinatario_correo,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'tiempo_servicio': instance.tiempo_servicio,
            'estado_decodificado': instance.estado_decodificado,
            'estado_decodificado_alerta': instance.estado_decodificado_alerta,
            'latitud': instance.latitud,
            'longitud': instance.longitud,
            'orden': instance.orden,
            'distancia_proxima': instance.distancia_proxima,            
            'franja_codigo': instance.franja_codigo
        }    
    
