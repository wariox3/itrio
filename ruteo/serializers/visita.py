from rest_framework import serializers
from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from ruteo.models.franja import RutFranja
from general.models.ciudad import GenCiudad

class RutVisitaSerializador(serializers.HyperlinkedModelSerializer):    
    destinatario_correo = serializers.CharField(allow_null=True)
    destinatario_direccion = serializers.CharField(allow_null=True, allow_blank=True)
    documento = serializers.CharField(allow_null=True)
    despacho = serializers.PrimaryKeyRelatedField(queryset=RutDespacho.objects.all(), default=None, allow_null=True)
    franja = serializers.PrimaryKeyRelatedField(queryset=RutFranja.objects.all(), default=None, allow_null=True)    
    ciudad = serializers.PrimaryKeyRelatedField(queryset=GenCiudad.objects.all())
    
    class Meta:
        model = RutVisita
        fields = ['id', 'guia', 'fecha', 'documento', 'destinatario', 'destinatario_direccion', 
                  'destinatario_telefono', 'destinatario_correo', 'peso', 'volumen', 'latitud', 'longitud', 'estado_decodificado', 
                  'orden', 'distancia_proxima',
                  'ciudad', 'despacho', 'franja']

    def to_representation(self, instance):        
        return {
            'id': instance.id,  
            'guia': instance.guia,
            'fecha': instance.fecha,
            'documento': instance.documento,
            'destinatario': instance.destinatario,
            'destinatario_direccion': instance.destinatario_direccion,
            'ciudad_id': instance.ciudad_id,
            'destinatario_telefono': instance.destinatario_telefono,
            'destinatario_correo': instance.destinatario_correo,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'estado_decodificado': instance.estado_decodificado,
            'latitud': instance.latitud,
            'longitud': instance.longitud,
            'orden': instance.orden,
            'distancia_proxima': instance.distancia_proxima
        }
    
