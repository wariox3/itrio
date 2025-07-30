from rest_framework import serializers
from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from general.models.ciudad import GenCiudad

class RutVisitaSerializador(serializers.ModelSerializer):    
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True, allow_null=True, default=None)
    
    class Meta:
        model = RutVisita
        fields = ['id', 'numero', 'fecha', 'documento', 'destinatario', 'destinatario_direccion', 'destinatario_direccion_formato', 
                  'destinatario_telefono', 'destinatario_correo', 'peso', 'volumen', 'cobro', 'tiempo', 'tiempo_servicio', 'tiempo_trayecto',
                  'latitud', 'longitud', 'orden', 'distancia', 'ciudad', 'ciudad__nombre' , 'despacho', 'franja_id', 'franja_codigo', 'resultados',
                  'datos_entrega', 
                  'estado_decodificado', 'estado_novedad', 'estado_devolucion', 'estado_decodificado_alerta', 
                  'estado_entregado', 'estado_entregado_complemento', 'estado_despacho']
        select_related_fields = ['despacho', 'ciudad']



class RutVisitaExcelSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutVisita

    def to_representation(self, instance): 
        ciudad_nombre = ''
        if instance.ciudad:
            ciudad_nombre = instance.ciudad.nombre     
        return {
            'id': instance.id,  
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
            'estado_despacho': instance.estado_despacho,
            'estado_entregado': instance.estado_entregado,
            'estado_novedad': instance.estado_novedad,
            'estado_devolucion': instance.estado_devolucion,            
            'latitud': instance.latitud,
            'longitud': instance.longitud,
            'orden': instance.orden,
            'distancia_proxima': instance.distancia_proxima,            
            'franja_codigo': instance.franja_codigo
        }    
    
class RutVistaTraficoSerializador(serializers.ModelSerializer):    
    class Meta:
        model = RutVisita
        fields = ['id', 'fecha', 'numero', 'documento', 'destinatario', 'destinatario_direccion', 'destinatario_telefono', 'estado_entregado', 'estado_novedad']